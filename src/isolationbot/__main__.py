import deltachat


class AutoReplyPlugin:
    @deltachat.account_hookimpl
    def ac_incoming_message(self, message: deltachat.Message):
        message.account.set_avatar("assets/avatar.jpg")
        message.create_chat()
        reply = "Sorry, sending messages to other servers than try.webxdc.org is not " \
            "supported on this server. If you want to try out Delta Chat, just create" \
            " another try.webxdc.org account to send messages back and forth. If you " \
            "have questions, please contact postmaster@try.webxdc.org."
        message.chat.send_text(reply)


def main(argv=None):
    deltachat.run_cmdline(argv=argv, account_plugins=[AutoReplyPlugin()])


if __name__ == "__main__":
    main()
