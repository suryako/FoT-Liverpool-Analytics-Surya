# FoT-Liverpool-Analytics-Surya

**Visualisation code for my winning entry to the Liverpool Analytics Challenge by Friends of Tracking. Optimised for x6 speedup.**

[Link to submission on Medium](https://medium.com/@kocherlakota/how-do-you-defend-against-liverpool-36c1a6996638)  
[Walkthrough of winning submissions on Friends of Tracking](https://youtu.be/AFm3JNPu9Jw?t=8m16s)

<br/>

## Visualisation Code
This repo is for recreating the Pitch Control videos shown above, with a x6 speedup<sup>1</sup> from using Python's ```joblib```.

To get started, clone this repo, including submodules<sup>2</sup> using:
```
git clone --recurse-submodules https://github.com/suryako/FoT-Liverpool-Analytics-Surya.git
```
<br/>

Install requirements and start a jupyter session with:
```
pip install -r requirements.txt
jupyter lab
```
<br/>

Open ```main_notebook.ipynb``` and run the cells in the notebook sequentially.  
The Pitch Control videos will be generated at ```goals_pc/_____.mp4```  
The notebook will allow you to interact with the data to get a better feel for it.

<br/>

 ## Acknowledgements
 Many thanks to [David Sumpter](https://www.david-sumpter.com/) and [Friends of Tracking](https://www.youtube.com/channel/UCUBFJYcag8j2rm_9HkrrA7w/about) for organising this, Ricardo Tavares for providing the dataset, and Laurie Shaw for the visualisation library.

<br/>

 ## Footnotes



 <sup>1</sup>
 x6 speedup on quad-core MacBook Pro with 8 vCPUs, increase ```n_jobs``` accordingly if you have even more CPU cores.

 <sup>2</sup>
 The [dataset by Ricardo](https://github.com/Friends-of-Tracking-Data-FoTD/Last-Row), and [Ciaran's data format converter](https://github.com/ciaran-grant) are included as submodules, locked at specific commit tags for reproducibility.  
  [Laurie's code (and Pitch Control model)](https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking) is directly included in this repo, to keep track of some of my changes that are specific to the Liverpool goal data.
