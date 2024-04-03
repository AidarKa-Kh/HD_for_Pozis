from django.urls import path
from . import views


urlpatterns = [
    path('ticket-details/<int:pk>/', views.ticket_details, name='ticket-details'),
    path('create-ticket/', views.create_ticket, name='create-ticket'),
    path('update-ticket/<int:pk>/', views.update_ticket, name='update-ticket'),
    path('all-tickets/', views.all_tickets, name='all-tickets'),
    path('ticket-queue/', views.ticket_queue, name='ticket-queue'),
    path('accept-ticket/<int:pk>', views.accept_ticket, name='accept-ticket'),
    path('close-ticket/<int:pk>', views.close_ticket, name='close-ticket'),
    path('workspace/', views.workspace, name='workspace'),
    path('blocked-tickets/', views.blocked_tickets, name='blocked-tickets'),
    path('all-closed-tickets/', views.all_closed_tickets, name='all-closed-tickets'),
    path('ticket/<int:pk>/delete/', views.delete_ticket, name='delete-ticket'),
    path('knowledge-base/', views.knowledge_base, name='knowledge-base'),
    path('knowledge-base/delete/<int:pk>/', views.delete_instruction, name='delete-instruction'),
    path('block-ticket/<int:pk>/', views.block_ticket, name='block-ticket'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
]