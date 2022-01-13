# Google-Play-Apps_Streamlit_Data_App

This dash app provides useful insight about Google Play Store Apps. Original data is derived from kaggle and can be found at the following link: https://www.kaggle.com/lava18/google-play-store-apps. The user can select the values of some parameters and changes on the plots will take place on the spot.

**Parameters**<br />
* Category <br />
The user may select the category of the apps which they are interested in (from the drop down menu).<br />
“*”Price <br />
The maximum price based on which results will be presented may be selected as well. Before converting, the values from string to float type, regex (a powerful library for string manipulation) was used.<br />
“*”Size <br />
Besides price, size is another parameter of the app. Given that, units varied (kb and Mb), additional string manipulation was performed via regex. Some other values were changed manually so that regex can run smoothly. <br />
“*”Latest date of update <br />
The user may select the latest date an update took place for the app. <br />
“*”Android version  <br />
Due to the high number of android versions, grouping was executed via regex to make the analysis easier (and the plots readable) given that it is only for educational purposes. Grouping was performed based on the first digit of Android version. It is worthwhile mentioning that there is a checkbox whether option " Varies with size" will be included in the pie plot.

**Results**
“*”Barplot
The first figure is a bar plot which depicts the reviews of the 5 apps with the highest ratings. 
“*”Pie plot
It shows the apps with


