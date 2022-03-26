# Setting up MyAnimeList App
This guide will help you create an app within MyAnimeList so you can use their API.<br />
You would need a MyAnimeList's account to continue.<br />

## Step 1: Creating the app
Head over to [https://myanimelist.net/apiconfig](https://myanimelist.net/apiconfig).<br />
Click on `Create ID`.<br />
![screenshot!!](/installation_guide/static/create_id.png)
<br />

## Step 1.1: Setting the details
Give your app a name and a description.<br />
> Note: Description must be atleast 50 characters and not over 500 characters.

Make sure `App type` is set to `web`.<br />
<br />
Set `App Redirect URL` and `Homepage URL` both to `https://myanimelist.net` (WORD FOR WORD, CASE SENSITIVE).<br />
Select `non-commercial` in the `Commercial / Non-Commercial` dropdown.<br />
Fill in the `Name / Company Name` field however your heart desires.<br />
Setting `Purpose of Use` to `hobbyist` sounded the most logical to me.<br />
<br />
You may ignore the fields that are optional (denoted by the absence of a red asterisk).<br />
<br />
Read through the `API License and Developer Agreement` ~your choice ლ(╹◡╹ლ).<br />
You'd need to agree with it to move on, so.... its for the better good.<br />
<br />
After all that is done, hit the `Submit` button located at the bottom and followed by `Return to list`.<br />
<br />
## Step 2: Retrieving the CLIENT_ID and CLIENT_SECRET
Upon returning back to list, you would see your app listed under the section `Clients Accessing the MAL API`.<br />
Edit your app.<br />
![screenshot!!](/installation_guide/static/edit_app.png)
<br />
You now have your `CLIENT_ID` and `CLIENT_SECRET`

[Back to the main guide you go!](https://github.com/FadedJayden/AP_MALPorter#step-1-setting-up-myanimelists-app)