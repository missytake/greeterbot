import deltachat


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


def main(argv=None):
    deltachat.run_cmdline(argv=argv, account_plugins=[AutoReplyPlugin()])


if __name__ == "__main__":
    main()
