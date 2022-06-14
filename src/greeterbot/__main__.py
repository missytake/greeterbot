import deltachat
from mailadm.mailcow import MailcowConnection
from time import sleep
import configargparse


class AutoReplyPlugin:
    @deltachat.account_hookimpl
    def ac_incoming_message(self, message: deltachat.Message):
        message.account.set_avatar("assets/avatar.jpg")
        message.create_chat()
        replytext = "Sorry, sending messages to other servers than try.webxdc.org is not " \
            "supported on this server. If you want to try out Delta Chat, just create" \
            " another try.webxdc.org account to send messages back and forth. If you " \
            "have questions, please ask around at https://support.delta.chat."
        reply = deltachat.message.Message.new_empty(message.account, "text")
        reply.quote = message
        reply.set_text(replytext)
        message.chat.send_msg(reply)


class GreetPlugin:
    def __init__(self, mailcow_endpoint, mailcow_token, dbpath):
        self.running = False
        self.mailcow = MailcowConnection(mailcow_endpoint, mailcow_token)
        self.dbpath = dbpath

    @deltachat.account_hookimpl
    def ac_process_ffi_event(self, ffi_event):
        if self.running is False:
            print("trying to create account...")
            account = deltachat.account.Account(self.dbpath)
            account.start_io()
            domain = account.get_config("addr").split("@")[1]
            self.running = True
            print("waiting for new mailcow users")
            while 1:
                sleep(5)
                users = self.mailcow.get_user_list()
                for user in users:
                    if user.addr == account.get_config("addr"):
                        # ignore self
                        continue
                    if user.addr.split("@")[1] != domain:
                        # ignore users from other domains
                        continue
                    if user.addr not in [c.addr for c in account.get_contacts()]:
                        print("Inviting", user.addr)
                        contact = account.create_contact(user.addr)
                        chat = contact.create_chat()
                        chat.send_text("Welcome to %s! Here you can try out webxdc." %
                                       (domain,))
                        chat.send_text("I prepared some for you:")
                        chat.send_file("assets/draw.xdc")
                        print("draw.xdc sent")


def main(argv=None):
    args = configargparse.ArgumentParser()
    args.add_argument("--mailcow-endpoint", env_var="MAILCOW_ENDPOINT", required=True,
                      help="the API endpoint of the mailcow instance")
    args.add_argument("--mailcow-token", env_var="MAILCOW_TOKEN", required=True,
                      help="you can get an API token in the mailcow web interface")
    args.add_argument("--email", required=True, help="the bot's email address")
    args.add_argument("--password", required=True, help="the bot's password")
    args.add_argument("--show-ffi", action="store_true", help="print Delta Chat log")
    args.add_argument("db_path", help="location of the Delta Chat database")
    options = args.parse_args()

    print(options)
    greet_plugin = GreetPlugin(options.mailcow_endpoint,
                               options.mailcow_token,
                               options.db_path)
    deltachat.run_cmdline(argv=argv, account_plugins=[AutoReplyPlugin(), greet_plugin])


if __name__ == "__main__":
    main()
