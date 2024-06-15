---
sort: 1
---
# 计算机是怎么工作的？

BUT HOW DO IT KNOW?

计算机是怎样工作的？

（更贴切的标题：**计算机为什么能理解程序员写的程序呢？**）

The Basic Principles of Computers For Everyone

让楼下老奶奶都能看明白的计算机工作原理介绍。

## 我的前言

我一直想亲自设计一个CPU，设计一套可以用的计算机系统，但是又缺少整体的指南以及细节上的参考。直到我看到了这本书。

遗憾的是这本书是英文版，在中文社区里没有看到完整的翻译版本。冥冥之中，我觉得这本书会可能会帮助我实现手工搭CPU的梦想（虽然我英语很差，但是我看得懂里面的电路图）。

正好这段时间（2022.7）我在steam上发现了一个很有意思的游戏[Virtual Circuit Board](https://store.steampowered.com/app/1885690/Virtual_Circuit_Board/)，这更像是一个数字电路仿真器而不是一个游戏。搭建CPU的时机已经成熟，接下来的一段时间，就要着手实现这个事情了。

在搭建的同时，顺便翻译下这本书，机翻为主，适当的做一些本土化的调整。翻译的同时，把搭建好的模块电路作为插图。

## Introduction

**书的前言**

The title of this book is the punch line of an old joke that goes like this:

Joe is a very nice fellow, but has always been a little slow. He goes into a store where a salesman is standing on a soapbox in front of a group of people. The salesman is pitching the miracle new invention, the Thermos bottle. He is saying, "It keeps hot food hot, and cold food cold...." Joe thinks about this a minute, amazed by this new invention that is able to make a decision about which of two different things it is supposed to do depending on what kind of food you put in it. He can’t contain his curiosity, he is jumping up and down, waving his arm in the air, saying “but, but, but, but…” Finally he blurts out his burning question "But how do it know?"

有这么一个小故事：

有个帅小伙人很不错，除了有点呆，反应比较慢。他来到一个商店看到售货员在给一群人推销保温杯：“保温杯冬天放热水，夏天能放雪糕。保冷又保热”。这帅小伙想了一会儿, 觉得保温杯很神奇，因为它能知道放进去的东西是冷的还是热的。帅小伙觉得自己想明白的保温杯的原理，高兴的手舞足蹈，但是又抑制不住内心的好奇，问道: “但是保温杯是怎么知道放进去的东西是冷的还是热的呢？”

这本书的标题源自于这个笑话。

```note
计算机为什么能看懂程序员写的程序呢？

我觉得这更嵌合这个小笑话。事实上，计算机不需要理解程序员写的程序，计算机也根本不知道一段程序在干嘛，他只是重复的取指令，执行，取下一条指令，执行。
```

You may or may not have laughed at the joke, but the point is that Joe looked at what this Thermos bottle could do, and decided that it must be capable of sensing something about its contents, and then performing a heating or cooling operation accordingly. He thought it must contain a heater and a refrigerator. He had no idea of the much simpler principle on which it actually operates, which is that heat always attempts to move from a hotter area to a cooler area, and all the Thermos does is to slow down this movement. With cold contents, the outside heat is slowed on its way in, and with hot contents, the heat is slowed on its way out. The bottle doesn't have to "know" in order to fulfill its mission, and doesn't heat or cool anything. And eventually, the contents, hot or cold, do end up at room temperature. But Joe's concept of how the bottle worked was far more complicated than the truth.

So the reason for the book title, is that when it comes to computers, people look at them, see what they can do, and imagine all sorts of things that must be in these machines. Or they imagine all sorts of principles that they must be based on, and therefore what they may be capable of. People may assign human qualities to the machine. And more than a few find themselves in situations where they feel that they are embarrassing themselves, like our friend in the joke, Joe.

不知道你笑没笑。这个帅小伙想的是保温杯先判断放进去的东西是冷的还是热的，如果是冷的那么制冷，如果是热的那么加热。但他没有注意到保温杯只是减缓热量的传递过程。保温杯不必知道自己装的是什么东西，也不需要加热制冷。保温杯里的东西最终都会变成和室温一样的温度，这个帅小伙把保温杯的原理想复杂了。

为何起这个标题呢（计算机为什么能理解程序员写的程序呢？）？当人们看到计算机运行着复杂的程序，像帅小伙一样开始思考计算的原理，脑补出这些计算机为了运行程序要做的事情、要遵循的各种法则，甚至认为电脑是不是和人脑一样有人的思想，来看懂程序员写的程序。学过一些计算机原理后，很多人应该会发现自己和这个帅小伙一样，把计算机想复杂了。

But computers are actually quite easy to understand. Of course computers have a greater number of parts than a Thermos bottle, but each part is extremely simple, and they all operate on a very simple, very easy to understand principle.

With the Thermos, the principle is that of the motion of heat. This is something we can observe in life. We see ice cubes melting when they are removed from the freezer, and we see the hot meal cooling off on the table when the family is late for dinner.

In the computer, the principle on which it operates has to do with electricity, but that doesn't mean that it is hard to understand. If you have observed the fact that when you turn on a light switch, a light bulb lights up, and when you turn the switch off, the light goes dark, then you have observed the principle on which computers operate. That is about all you need to know about electricity to understand computers.

电脑的零件倒是比保温杯多，但是这些零件（逻辑门）的工作原理都非常好理解。

热水瓶的原理是降低热传递速度。热量传递这个现象可以观察的到比如冰块融化；热菜变冷。

计算机的基本原理和电相关，电虽然比较抽象但是也可以通过一些方法观察的到。比如按下墙上的开关，灯泡就会亮起来；关掉开关灯就会熄灭。这种开关的对应逻辑就是理解计算机工作原理用到的所有与电路相关的知识。

```note
老外写书把大家都当小学生，这倒是挺好，但是有些地方总是会显得讲了半天没重点。我感觉这里就是。这里要表达的意思：研究计算机原理不需要三极管、晶体管等电路知识，虽然晶体管才是CPU内部的基本单元。

我们再往上走一步，把晶体管封装成的逻辑门看作CPU的最小单位就好了。
```


## 书的介绍

This book is not primarily intended to be a textbook. There are no problems to do at the end of each chapter. Its intention is simply to demystify the subject of computers for anyone who has ever wondered what’s going on inside of that box. Of course, it also makes aperfect introduction to computers for a young person who will ultimately go on to get a PhD in Computer Science. But it should be easily understandable by house wives,s enior citizens and children who can read well. It should be understandable to plumbers and street sweepers. It requires no previous technical education. It only requires that you can read the language, you can turn a light bulb on and off, and you can do very simple addition on the order of 8+5=13.

This book presents the complete essentials that make upa computer. It presents every piece and part, in the proper order so that each one will make sense, and can be understood. Every part is explained fully, and every new word is defined thoroughly when it is first used. Any attempt to simplify the subject further would leave gaps in the big picture where someone would still have to guess how the parts work together, and you just wouldn’t ever have that “Aha, I get it!” moment that I think you’ll soon have.

This book is not a ‘dumbed-down’ version of some college textbook. It is a complete explanation of the basic principles of computers. It is a technical book, but sois a cookbook and so is a driver’s education handbook.This book just starts at the beginning and defines everyitem needed to understand the machine. No matter what someone already knows about computers, this will fill inany missing pieces and put them all together into something that makes sense.

这并不是一本教科书，也不会有课后习题。这本是为对计算机感兴趣的人、想了解计算机工作原理的人准备的。当然计算机专业的同学也可以使用这本书来学习计算机的全貌。最重要的，这本书里的内容很好理解，楼下的老奶奶，二年级的小朋友都能看明白。也就是说这本书不需要太多的前置知识，只要看得懂中文，明白打开开关灯就会亮，会十以内加减法就可以。

这本书以从逻辑门开始，逐步实现构成计算机的每一个部分。每部分都介绍的非常详细而且易于理解。都一个全新的名词出现的时候，都会进行详细的解释。当子模块用简化框图表示以实现更复杂的模块时，都会配上完美的插图来帮助理解这几部分时如何配合工作的。

这本书并不是简化版的计算机专业的教科书。这本书对对计算机工作原理做了完整的说明，像一本手册，从一开始就解释了计算机里面需要理解的东西。如果你已经有了一些计算机底层的知识，那么这本书会填满你所有关于底层缺失的部分，形成一个完成的计算机体系。

Even our friend, Joe, could understand this book withdiligent study. There are thousands of words and ideasassociated with the field of computers that make thewhole subject seem like a mess. But the basic conceptsunderlying them are simple.

In this book, there will not be volumes of trivia about the construction or history of computers, just theessentials, no more and no less. Each part of thecomputer has a simple function, and when they areconnected together, you end up with a useful machinecalled a computer.

There is nothing to memorize in this book. Each chapteris designed to give you a new idea that you didn’t havebefore, or if it is something that you had heard aboutpreviously, it always seemed confusing. Each idea isvery simple, and one thing leads to the next. Eachchapter presents an idea. Each idea is simple and easyto understand. Later chapters present ideas that buildon the ideas from previous chapters.

楼下老奶奶也能通过勤奋学习理解书里的内容。尽管计算机领域的术语很多，体系结构看起来复杂且混乱，但是背后的基本概念很简单。

这本书里不会出现计算机的历史等内容，只有构成计算机必要的部分。每一部分都有一个简单的功能，当你把它们连接到一起时，就能获得一个有用的机器，这就是计算机。

这本书里没有需要背诵的东西，每一章都是一个新的想法，每个想法都很简单，一个接着一个环环相扣。后面的章节提出的概念基于先前章节提出过的概念。

If someone were to write a book about how to build ahouse, there could be various levels of detail. Thesimplest book would say, “lay a foundation, put up thewalls, cover with a roof, put in plumbing andelectrical, and you’re done.” That would not be enoughdetail for someone who didn’t already have someexperience using a hammer and saw and installing afaucet and wiring a light switch.

At the other end of the spectrum would be a book thathad separate chapters for every possible type offoundation, the different kinds of dirt you might haveto dig in, formulas for a dozen different kindsconcrete, charts of weather conditions that are optimumfor laying foundations, etc. That would be far too muchinformation. There would be so many details, that whatwas really important would get lost.

如果有人写了一本盖房子的书，会包含不同层次的细节。最简单的那本这么写：“打地基，砌墙，封顶，通水电，就完成了。” 有些人榔头也没见过，民用电电压是多少也不知道，因此这么写这些细节还不够。

另一种写法是事无巨细，你可能需要挖掘的不同类型的泥土，十几种不同类型混凝土的公式，最适合奠定基础的天气条件图表，等等。这些信息太多了。太多的细节又会让重点丢失，因此这个度还是很难把握的。

This book attempts to give just enough detail to seewhat every computer has in common and how they work, nothow to build the biggest or best computer ever made. Itis not about any specific brand of computer. It is not about how to use a computer. If it were a book about building a house, it would probably describe a simple plan for a sturdy garden shed with a sink and one barelight bulb, showing the size and shape of every piece of wood, where to put all the nails, how to hang the door and how to put the water pipes together so they wouldn’t leak. It would not show how to build anything as complicated as a fancy curved oak staircase.

We are going to show the one simple part that computers are made of, and then connect a bunch of them together until we have built a complete computer. It is going tobe a lot simpler than you ever imagined.

这本书试图提供足够的细节来说明计算机的工作原理，去尝试设计一台简单计算机。麻雀虽小五脏俱全，照着这本书没法设计一台最大或最好的计算机。但是工作原理和具体品牌的电脑无关，但是具体品牌的电脑又基于这些原理实现。

书里展示计算机的每一个简单模块是如何工作的，然后把这些模块连接起来，一台能用的计算机就出现了。



