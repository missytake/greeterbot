import time

import deltachat
from deltachat.tracker import ConfigureFailed
from mailadm.mailcow import MailcowConnection
from time import sleep
import tempfile
import os
import configargparse
import pkg_resources


def setup_account(addr: str, app_pw: str, data_dir: str, debug: bool) -> deltachat.Account:
    """Create an deltachat account with a given addr/password combination.

    :param addr: the email address of the account.
    :param app_pw: the SMTP/IMAP password of the accont.
    :param data_dir: the directory where the data(base) is stored.
    :param debug: whether to show log messages for the account.
    :return: the deltachat account object.
    """
    try:
        os.mkdir(os.path.join(data_dir, addr))
    except FileExistsError:
        pass
    db_path = os.path.join(data_dir, addr, "db.sqlite")

    ac = deltachat.Account(db_path)
    if debug:
        ac.add_account_plugin(deltachat.events.FFIEventLogger(ac))
    if not ac.is_configured():
        ac.set_config("addr", addr)

    ac.set_config("mvbox_move", "0")
    ac.set_config("sentbox_watch", "0")
    ac.set_config("bot", "1")
    ac.set_config("mdns_enabled", "0")

    if app_pw != ac.get_config("mail_pw") or not ac.is_configured():
        ac.set_config("mail_pw", app_pw)
        configtracker = ac.configure()
        try:
            configtracker.wait_finish()
        except ConfigureFailed as e:
            print(
                "configuration setup failed for %s with password:\n%s"
                % (ac.get_config("addr"), ac.get_config("mail_pw"))
            )
            raise
    ac.start_io()
    avatar = pkg_resources.resource_filename(__name__, "avatar.jpg")
    ac.set_avatar(avatar)
    ac.set_config("displayname", "Hello at try.webxdc.org!")
    return ac


class GreetBot:
    def __init__(self, mailcow_endpoint, mailcow_token, account):
        self.mailcow = MailcowConnection(mailcow_endpoint, mailcow_token)
        self.account = account
        self.domain = account.get_config("addr").split("@")[1]

    def greet_users(self):
        users = self.mailcow.get_user_list()
        for user in users:
            if not user.addr:
                # skip broken accounts
                continue
            if user.addr == self.account.get_config("addr"):
                # ignore self
                continue
            if user.addr.split("@")[1] != self.domain:
                # ignore users from other domains
                continue
            if user.addr not in [c.addr for c in self.account.get_contacts()]:
                time.sleep(20)  # wait until Delta is configured on the user side
                print("Inviting", user.addr)
                contact = self.account.create_contact(user.addr)
                chat = contact.create_chat()
                chat.send_text("Welcome to %s! Here you can try out webxdc." % (self.domain,))
                chat.send_text("I prepared some for you:")
                chat.send_file(pkg_resources.resource_filename(__name__, "checklist.xdc"))
                chat.send_file(pkg_resources.resource_filename(__name__, "tower-builder.xdc"))
                chat.send_text(
                    "You can send a message to xstore@testrun.org to discover more apps! "
                    "Some of these games you can also play with friends, directly in the chat."
                )


def main():
    args = configargparse.ArgumentParser()
    args.add_argument(
        "--mailcow-endpoint",
        env_var="MAILCOW_ENDPOINT",
        required=True,
        help="the API endpoint of the mailcow instance",
    )
    args.add_argument(
        "--mailcow-token",
        env_var="MAILCOW_TOKEN",
        required=True,
        help="you can get an API token in the mailcow web interface",
    )
    args.add_argument("--email", help="the bot's email address", env_var="DELTACHAT_ADDR")
    args.add_argument("--password", help="the bot's password", env_var="DELTACHAT_PASSWORD")
    args.add_argument("--db_path", help="location of the Delta Chat database")
    args.add_argument("--show-ffi", action="store_true", help="print Delta Chat log")
    ops = args.parse_args()

    # ensuring account data directory
    if ops.db_path is None:
        tempdir = tempfile.TemporaryDirectory(prefix="hellobot")
        ops.db_path = tempdir.name
    elif not os.path.exists(ops.db_path):
        os.mkdir(ops.db_path)

    ac = setup_account(ops.email, ops.password, ops.db_path, ops.show_ffi)
    greeter = GreetBot(ops.mailcow_endpoint, ops.mailcow_token, ac)
    print("waiting for new mailcow users...")
    while 1:
        greeter.greet_users()
        sleep(5)


if __name__ == "__main__":
    main()
