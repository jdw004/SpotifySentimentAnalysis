import numpy
from taipy.gui import Gui, notify

import pandas as pd

page = """
<page|layout|columns=300px 1fr|
<|sidebar|
### **Filters 🔎**{: .blue}
<|{x_selected}|selector|gap=30px|lov={select_x}|dropdown|label=Select x|>
<|{x_selected}|selector|gap=30px|lov={select_x}|dropdown|label=Select x|>
<br/>

|>

<|container|
# **Lyric**{: .blue} Vibe ✨🎶

Tune into your emotions.

<br/>

<|layout|columns=1 1 1|gap=30px|class_name=card|
<placeholder|
## **Placeholder**{: .blue}

<|{placeholder}|input|label=Placeholder|>
|placeholder>

<mood|
## **Mood**{: .blue}

<|{mood}|input|label=How do you think you feel?|>
|mood>

<style|
## **Spotify**{: .blue} Handle

<|{style}|input|label=Type your Spotify Handle...|>
|style>

<|Generate text|button|label=Generate Your Vibe!|>
|>

<br/>

---
### Global Map of **Happiness**{: .blue}
---
<br/>

### Generated **Information**{: .blue}

<|{tweet}|input|multiline|label=Results|class_name=fullwidth|>

|>
<br/>

"""

# my_theme = {
#   "palette": {
#     "background": {"default": "#808080"},
#     "primary": {"main": "#a25221"}
#   }
# }

my_theme = {
  "palette": {
    "background": {"default": "#4682b4"},
    "primary": {"main": "#4682b4"}
  },
  ".blue": {
    "color": "blue"
  }
}

stylekit = {
  "color_primary": "#BADA55",
  "color_secondary": "#C0FFE",
  "font-family": "Space Grotesk"
}

Gui(page).run(theme=my_theme, stylekit=stylekit)
