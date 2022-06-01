# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from tokenize import String
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions

class Products():
    def __init__(self):
        self.product_name = ""
        self.product_options = ["version","support","license"]
        self.fake_database = {
            "version":{
                "fidessa":10.2,
                "triplepoint" : 18.9
            },
            "support":{
                "fidessa":"https://iongroup.com/markets/products/fidessa/",
                "triplepoint" : "https://www.tpt.com/products/agriculture/"
            },
            "license":{
                "fidessa":"contact xyz",
                "triplepoint" : "contact abc"
            }
            
        }
    def handle_input(self,options) -> str:
        if options == "version":
            return self.handle_version()
        elif options == "support":
            return self.handle_support()
        else :
            return self.handle_license()
    def handle_version(self) -> str:
        return self.fake_database["version"][self.product_name]
    def handle_license(self) -> str:
        return self.fake_database["support"][self.product_name]
    def handle_support(self) -> str:
        return self.fake_database["license"][self.product_name]


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    def __init__(self) -> None:
        super().__init__()
        self.ProductObj = Products()


    async def on_message_activity(self, turn_context: TurnContext):
        text: str = turn_context.activity.text
        if text == "ion":
            await turn_context.send_activity("Ion is a great organization\nMore information at https://iongroup.com/")
            await self.send_global_cards(turn_context)
        elif text == "product":
            await self.send_product_cards(turn_context)
        elif text == "triplepoint" or text == "fidessa":
            self.ProductObj.product_name = text
            await self.send_product_info_cards(turn_context)
        elif text in self.ProductObj.product_options:
            await turn_context.send_activity(f"{self.ProductObj.handle_input(text)}") 
            await self.send_global_cards(turn_context)
        else:
            await turn_context.send_activity(f"Hey! there")

    async def send_product_cards(self, turn_context: TurnContext):
        reply = MessageFactory.text("What do you want to know about the product?")
        reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="TriplePoint",
                        type=ActionTypes.im_back,
                        value="triplepoint",
                        image="https://iongroup.com/wp-content/uploads/2016/09/iON_HBlu_Blu_Org@2x.png",
                        image_alt_text="triplepoint",
                        ),
                    CardAction(
                        title="Fidessa",
                        type=ActionTypes.im_back,
                        value="fidessa",
                        image="https://iongroup.com/wp-content/uploads/2016/09/iON_HBlu_Blu_Org@2x.png",
                        image_alt_text="fidessa",
                        )
                    ]
                )
        return await turn_context.send_activity(reply)
    async def send_product_info_cards(self, turn_context: TurnContext):
        reply = MessageFactory.text("What do you want to know about the product?")

        reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="version information",
                        type=ActionTypes.im_back,
                        value="version",
                        image="https://iongroup.com/wp-content/uploads/2016/09/iON_HBlu_Blu_Org@2x.png",
                        image_alt_text="version",
                        ),
                    CardAction(
                        title="licensing information",
                        type=ActionTypes.im_back,
                        value="license",
                        image="https://iongroup.com/wp-content/uploads/2016/09/iON_HBlu_Blu_Org@2x.png",
                        image_alt_text="license",
                        ),
                    CardAction(
                        title="supported technology",
                        type=ActionTypes.im_back,
                        value="support",
                        image="https://iongroup.com/wp-content/uploads/2016/09/iON_HBlu_Blu_Org@2x.png",
                        image_alt_text="support",
                        ),
                    ]
                )
        return await turn_context.send_activity(reply)
    async def send_global_cards(self, turn_context: TurnContext):
        reply = MessageFactory.text("What do you want to know about?")

        reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title="ION Products",
                        type=ActionTypes.im_back,
                        value="product",
                        image="https://cdn-icons-png.flaticon.com/512/2103/2103478.png",
                        image_alt_text="product",
                        ),
                    CardAction(
                        title="organization",
                        type=ActionTypes.im_back,
                        value="ion",
                        image="https://iongroup.com/wp-content/uploads/2016/09/iON_HBlu_Blu_Org@2x.png",
                        image_alt_text="organization",
                        ),
                    ]
                )
        return await turn_context.send_activity(reply)

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
            ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await self.send_global_cards(turn_context)
