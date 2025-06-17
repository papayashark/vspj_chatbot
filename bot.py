from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from knowledge_base import KnowledgeBase

class MyBot(ActivityHandler):
    def __init__(self):
        super().__init__()
        self.knowledge_base = KnowledgeBase("knowledge.json")  # Load from JSON file

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Ahoj! Jsem váš pomocný chatbot. Zeptejte se mě na cokoliv ohledně školy.")

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text
        answer = self.knowledge_base.get_answer(user_message)

        if answer:
            await turn_context.send_activity(answer)
        else:
            await turn_context.send_activity("Omlouvám se, nenašel jsem odpověď na tuto otázku.")
