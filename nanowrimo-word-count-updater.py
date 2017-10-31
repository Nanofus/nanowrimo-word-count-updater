import sublime
import sublime_plugin
import http
import urllib
import hashlib

class PostWordCountCommand(sublime_plugin.TextCommand):
    def run(self, view):
        print("Starting to update NaNoWriMo word count...")
        sublime.status_message("Starting to update NaNoWriMo word count...")

        # Load settings
        global_settings = sublime.load_settings("nanowrimo.sublime-settings")
        secret_key = global_settings.get('nanowrimo_secret_key', "")
        name = global_settings.get('nanowrimo_name', "")

        # Show error if settings missing
        if (secret_key == ""):
            sublime.message_dialog("No NaNoWriMo secret key set. Please define it in the package settings.")
            return
            if (name == ""):
                sublime.message_dialog("No NaNoWriMo name set. Please define it in the package settings.")
                return

        # Count words
        text = self.view.substr(sublime.Region(0, self.view.size()));
        count = len(text.split())

        # Prompt for confirmation
        if (sublime.ok_cancel_dialog("Update NaNoWriMo word count based on this file? (" + str(count) + " words)") != sublime.DIALOG_YES):
            return

        # Generate hash
        api_string = secret_key + name + str(count)
        hash = hashlib.sha1(api_string.encode("utf-8"))

        # Make the request
        req = urllib.request.Request(url="https://nanowrimo.org/api/wordcount?hash=" + str(hash.hexdigest()) + "&name=" + name + "&wordcount=" + str(count), method="PUT")
        with urllib.request.urlopen(req) as f:
            pass
        print(f.status)
        print(f.reason)
        response_body = f.read()
        print(response_body)

        # Check results
        if ("{\"novel\"=>" in str(response_body)):
            sublime.status_message("NaNoWriMo word count updated to " + str(count) + " for user " + name)
            print("NaNoWriMo word count updated to " + str(count) + " for user " + name)
        else:
            sublime.status_message("Something went wrong with NaNoWriMo word count update, please check the console.")
            sublime.message_dialog("Something went wrong with NaNoWriMo word count update, please check the console.")
            print("NaNoWriMo: Something went wrong; response:")
            print("Word count: " + str(count))
            print("Hash for API: " + hash.hexdigest())
