# **Project ContentGen**

## **Problem Statement:**

According to HubSpot companies spend 46% of their budget on content creation (HubSpot, 2017) and 24% of marketers plan on increasing their investment in content marketing in 2020 (HubSpot, 2020). Content creation is obviously a very important aspect of the overall marketing plan for company. There are usually a lot of moving pieces that go into creating an effective content marketing plan such as photographers, editors, videographers, models, writers, etc. With all of this being said, there is a faster approach to creating content at scale. That is through GANs (Generative Adversarial Networks) and natural language processing text transformers such as GPT-2. 


## **Project Layout**

### Creating the Computer Generated Influncer:
There will be two parts of this project. The first part will be the computer generated influencer. I will be utilizing [StyleGan2](https://github.com/NVlabs/stylegan2) from NVIDIA. 


### Creating the Blog Post Generator:
Onto the second part of the project. This section of the project will enable a user of my application to pick a topic out of any of the topics available on Medium and my application will generate a 300 word body of text that they can use.

## **Data**

**Influencer Generation Data:**  
I will be using for the first inital run, the dataset provided by NVIDIA in their StyleGan2 repo. I will be looking for more face data or potentially even take pictures of my friends and get pictures of people from our cohort. For generating the bodies of the people I will be using this dataset [here](https://www.robots.ox.ac.uk/~vgg/data/pose/index.html#downloadlink). I am still working out the best way to download these files, either to an external hardrive or google drive. The video I will be using as my base for the TikTok video is [here](https://vm.tiktok.com/ZMJD8tqGu/).


**Tweet Generator:**  
Since I will be using GPT-2 as my tweet generator I will only need to train it on the tweets for a certain topic which I chose as art. After feeding it a handful of tweets it should begin to reply hopefully human-like.
