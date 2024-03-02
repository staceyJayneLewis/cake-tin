from django.http import HttpResponse

class StripeWebhook_Handler:
    """Manages the Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def manage_event(self, event):
        """Manage all types of webhook event"""

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
