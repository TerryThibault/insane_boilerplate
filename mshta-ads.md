# Goal
Detect when the mshta.exe executable is run an unusual and potentially malicious way.

# Categorization
These attempts are categorized as [Execution / Mshta](https://attack.mitre.org/techniques/T1170/).

# Strategy Abstract
The strategy will function as follows: 

* Collect Windows Event Logs related to the mshta executable. 
* Generate an alert if mshta is called from the command line and spawns a child process containing the words "PowerShell" or "VBScript".

# Technical Context
[HTML Applications](https://docs.microsoft.com/en-us/previous-versions//ms536496(v=vs.85)) are a means of delivering a browser-based application without being constrained by the internet browser security model. 

Microsoft initially developed the technology to bring Windows Internet Explorer to the fore as a viable windows development platform. HTAs are trusted and display any information that a web developer creates -- they contain all of the power of Internet Explorer without enforcing the strict security model and user interface of the browser. 

It is considered a feature that HTAs can bypass the normal security policies of the browser, and can directly manipulate a client machine. 

If HTAs are not used regularly, it is worth disabling the mshta.exe executable entirely. If HTAs are used from the command line, it would make sense to change the default program that a `.hta` program is run by (perhaps to notepad) so that a user is less likely to fall victim to a social engineering attack involving HTAs.

Because HTAs are executed by mshta.exe, a microsoft signed binary, it is possible for an adversary to bypass application whitelisting by crafting a custom hta file that runs PowerShell or VBA code.

Example:
```
<script language="VBScript">
    Function var_func()
        Dim var_shell
        Set var_shell = CreateObject("Wscript.Shell")
        var_shell.run "powershell.exe -nop -w hidden -encodedcommand [base64 encoded command]"
    End Function
    var_func
    self.close
</script>

<h1>Hello, world</h1>
```

In the above example, the HTML Application is running a base64 encoded powershell command, while displaying text that reads "Hello, world". The hta process will create a child process to run the powershell. 

# Blind Spots and Assumptions
This strategy relies on the following assumptions: 
* Windows event reporting is valid and trustworthy. 
* Windows event logs are being successfully generated on Windows hosts.
* Windows event logs are successfully forwarded to WEF servers. 
* SIEM is successfully indexing Windows event logs.

A blind spot will occur if any of the assumptions are violated. For instance, the following would not trip the alert: 
* Windows event forwarding or auditing is disabled on the host.
*  MSHTA is run without generating a Windows event log.

# False Positives
There are several instances where false positives will occur: 
* Users create custom HTML Applications that use PowerShell or VBScript.
* Users modify an already existing HTML Applications, adding PowerShell or VBScript. 

# Priority
The priority is set to medium under all conditions.

# Validation
Validation can occur for this ADS by saving the following as `test.hta`, and running it from the command line with `mshta.exe test.hta`:
```
<script language="VBScript">
    Function var_func()
        Dim var_shell
        Set var_shell = CreateObject("Wscript.Shell")
        var_shell.run "powershell.exe -nop -w hidden ipconfig"
    End Function
    var_func
    self.close
</script>

<h1>Hello, world</h1>
```

# Response
In the event that this alert fires, the following response procedures are recommended:
* Identify the PowerShell or VBScript that was executed by the offending HTML Application.
* If determined to be benign use of the mshta.exe, get a checksum of the HTML Application and add it to a list of known-good programs.
* If determined not to be benign use of mshta.exe, treat as a high priority alert.
  * Identify where the malicious HTML Application came from.
  * Ivestate any processes which are running on the offending device.

# Additional Resources
* https://en.wikipedia.org/wiki/HTML_Application
* http://blog.sevagas.com/?Hacking-around-HTA-files
