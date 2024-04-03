import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Ticket, DepartmentMembership, KnowledgeBase
from .form import CreateTicketForm, UpdatedTicketForm, KnowledgeBaseForm
from users.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


@login_required
def knowledge_base(request):
    instructions = KnowledgeBase.objects.all()
    form = KnowledgeBaseForm()

    if request.method == 'POST':
        form = KnowledgeBaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('knowledge-base')

    context = {'instructions': instructions, 'form': form}
    return render(request, 'ticket/knowledge_base.html', context)


@login_required
def delete_instruction(request, pk):
    if request.method == 'POST':
        instruction = KnowledgeBase.objects.get(pk=pk)
        instruction.delete()
    return redirect('knowledge-base')


@login_required
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    t = User.objects.get(username=ticket.created_by)
    tickets_per_user = t.created_by.all()

    if request.method == 'POST':
        form = UpdatedTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = UpdatedTicketForm(instance=ticket)

    # Проверка, принадлежит ли заявка текущему пользователю или является ли пользователь is_manager
    if (not request.user.is_superuser and ticket.created_by != request.user) and not request.user.is_manager:
        messages.warning(request, 'Ошибка! У вас нет прав для просмотра данной заявки!')
        return redirect('all-tickets')

    context = {'ticket': ticket, 'ticket_per_user': tickets_per_user, 'form': form}
    return render(request, 'ticket/ticket_details.html', context)


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.ticket_status = 'Sent'
            ticket.save()
            messages.info(request, 'Вы успешно создали заявку!')
            return redirect('all-tickets')
        else:
            messages.warning(request, 'Что-то пошло не так! Проверьте правильность заполнения формы!')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form': form}
        return render(request, 'ticket/create_ticket.html', context)


@login_required
def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if not ticket.is_resolved:
        if request.method == 'POST':
            form = UpdatedTicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                form.save()
                messages.info(request, 'Вы успешно обновили заявку!')
                if request.user.is_customer:
                    return redirect('all-tickets')
                else:
                    return redirect('ticket-queue')
            else:
                messages.warning(request, 'Что-то пошло не так!')
                return redirect('create_ticket')
        else:
            form = UpdatedTicketForm(instance=ticket)
            context = {'form': form}
            return render(request, 'ticket/update_ticket.html', context)
    else:
        messages.warning(request, 'Ошибка! У вас нет прав для изменения заявки!')
        return redirect('dashboard')


@login_required
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-date_created')
    context = {'tickets': tickets}
    return render(request, 'ticket/all_tickets.html', context)


@login_required
def blocked_tickets(request):
    if request.user.is_manager:
        departments = DepartmentMembership.objects.filter(user=request.user).values_list('department', flat=True)
        tickets = Ticket.objects.filter(department__in=departments, ticket_status='Blocked').order_by('-date_created')
    else:
        tickets = Ticket.objects.filter(created_by=request.user, ticket_status='Blocked').order_by('-date_created')
    context = {'tickets': tickets}
    return render(request, 'ticket/blocked_tickets.html', context)


@login_required
def ticket_queue(request):
    departments = DepartmentMembership.objects.filter(user=request.user).values_list('department', flat=True)
    if not departments:
        tickets = Ticket.objects.filter(ticket_status='Sent').order_by('-date_created')
    else:
        tickets = Ticket.objects.filter(department__in=departments, ticket_status='Sent').order_by('-date_created')
    context = {'tickets': tickets}
    return render(request, 'ticket/ticket_queue.html', context)


# удовлетворение заявки
@login_required
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Заявка успешно принята!')
    return redirect('workspace')


# закрытие заявки
@login_required
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved = True
    ticket.closed_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Заявка успешно обработана!')
    return redirect('ticket-queue')


# заявка в обработке
@login_required
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=False).order_by('-date_created')
    context = {'tickets': tickets}
    return render(request, 'ticket/workspace.html', context)


# все завершенные заявки
@login_required
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=True).order_by('-date_created')
    context = {'tickets': tickets}
    return render(request, 'ticket/all_closed_tickets.html', context)


# удаление заявки
@login_required
def delete_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if not ticket.is_resolved:
        ticket.delete()
        messages.info(request, 'Заявка успешно удалена!')
        return redirect('all-tickets')
    else:
        messages.warning(request, 'Ошибка! У вас нет прав для удаления заявки!')
        return redirect('dashboard')


@login_required
def block_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if ticket.ticket_status == 'Blocked':
        ticket.ticket_status = 'Sent'
        messages.info(request, 'Заявка успешно разблокирована!')
    else:
        ticket.ticket_status = 'Blocked'
        messages.info(request, 'Заявка успешно заблокирована!')

    ticket.save()
    return redirect('ticket-details', pk=pk)


def search(request):
    query = request.GET.get('q')

    # Ищем заявки и инструкции, содержащие введенный запрос в заголовке или описании
    tickets = Ticket.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    instructions = KnowledgeBase.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    context = {
        'tickets': tickets,
        'instructions': instructions,
        'query': query
    }

    return render(request, 'ticket/search_results.html', context)


def about(request):
    return render(request, 'ticket/about.html')