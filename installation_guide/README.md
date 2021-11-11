# Installation Guide

Installation guide made for dummies. :)<br />
This guide will cover on how to install [Git](https://git-scm.com/) and [Python](https://www.python.org/) to start using this simple and lightweight module.<br />
This guide uses resources readily available in the internet and is meant to aid you in setting up Python and Git in the operating system you're using.<br />
Refer to other sources at your own discretion.<br />

Operating systems:<br />
[Windows](https://github.com/ballgoesvroomvroom/AP_MALPorter/tree/main/installation_guide#windows)<br />
[Linux](https://github.com/ballgoesvroomvroom/AP_MALPorter/tree/main/installation_guide#linux)<br />
[macOS](https://github.com/ballgoesvroomvroom/AP_MALPorter/tree/main/installation_guide#macos)

## Windows
Installation time: ~10minutes<br />
<br />
This guide only covers Windows 10.<br />
Though earlier versions of Windows should be able to follow along<br />
Unless you're using Windows 98 or anything that is considered old in our modern society, you can check out [TortoiseGit](https://tortoisegit.org/docs/tortoisegit/tgit-intro-install.html) to install Git.
<br />
### First step: Getting Python
[https://www.python.org/downloads/](https://www.python.org/downloads/)<br />
The installer will help you get `Python` command running in your terminal (will be using Command Prompt for the entirety of this document)<br />
Make sure to install `pip` while you're at it.<br />
<br />
Now that you can run `Python` command in the command prompt, you can start running Python scripts/projects.<br />
So, moving onto getting the project.

### Second step: Installing Git
[GitHub's own guide](https://github.com/git-guides/install-git#install-git-on-windows)<br />
After managing to get Git installed, you can know clone this repository over to your local system.<br />

### Third step: Cloning the project into your local system
Navigate into the directory you want to put the project files into using the `cd` command.<br />
Lets say we want to put the entire project folder in the `Desktop` folder, our path to it is,<br />
`C:\Users\faded\Desktop`<br /><br />
Running this command will get us to the working directory.<br />
`cd C:\Users\faded\Desktop`<br />

![](/installation_guide/static/win_cd_cmd.png)

Then running,<br />
```git
git clone https://github.com/ballgoesvroomvroom/AP_MALPorter
```
Will get us the project file in `C:\Users\faded\Desktop`.<br />
And you're done!

---
## Linux
Installation time: ~5minutes<br />
<br />
Any Linux based operating system, CentOS, Debian, Ubuntu, Fedora, etc.<br />
Im under the assumption that anyone who uses Linux based OS is a technological savvy person so this portion of the guide seems pointless, however it exists nonetheless.<br />
<br />
### First step: Getting Python
[Actual dummies guide](https://www.dummies.com/programming/python/how-to-install-python-on-a-linux-system/)

### Second step: Installing Git
Git should come pre-installed.<br />
To verify the existence of Git, run the `git` command in your terminal.<br />

If it isn't installed, you can check out this:<br />
[GitHub's own guide](https://github.com/git-guides/install-git#install-git-on-linux)

### Third step: Cloning the project into your local system
Navigate to the working directory (the directory you want to put all the project files into).<br />
Using the `cd` command.<br />
<br />
After you've successfully navigated to the directory you want, run the following command to get the project.<br />
```git
git clone https://github.com/ballgoesvroomvroom/AP_MALPorter
```
And there you go, you have the project folder under the working directory.

---
## macOS
Installation time: ~6minutes<br />
<br />
### First step: Getting Python
[Actual dummies guide](https://www.dummies.com/programming/python/how-to-install-python-on-a-mac/)

### Second step: Installing Git
Git should come pre-installed with macOS.<br />
To verify the existence of Git, run the `git` command in your terminal.<br />

If it isn't installed, you can check out this:<br />
[GitHub's own guide](https://github.com/git-guides/install-git#install-git-on-mac)

### Third step: Cloning the project into your local system
Navigate to the working directory (the directory you want to put all the project files into).<br />
Using the `cd` command.<br />
<br />
After you've successfully navigated to the directory you want, run the following command to get the project.<br />
```git
git clone https://github.com/ballgoesvroomvroom/AP_MALPorter
```
And there you go, you have the project folder under the working directory.