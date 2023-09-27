import os

import matplotlib
import matplotlib.pyplot as plt

from code.analyse import user_analyse,frequency_text,emotion_text,hot_band

# if os.name == 'nt':
#     plt.rcParams['font.sans-serif'] = ['SimHei']
# else:
#     plt.rcParams['font.family'] = 'Arial Unicode MS'

font = {'family':'SimSun',
        'weight':'bold',
        'size':'9'}
plt.rc('font', **font)
plt.rc('axes', unicode_minus=False)


#用户发微博频率图像
def user_():
    list=user_analyse()
    time=[]
    num=[]
    up=[]
    comment=[]
    for line in list:
        time.append(line[0])
        num.append(line[1])
        up.append(line[2])
        comment.append(line[3])
    fig,axarr=plt.subplots(2,1)
    print(type(axarr[0]))
    axarr[0].set_title('用户微博分析')
    axarr[0].plot(time,num,label='发博数')
    axarr[0].grid()
    axarr[0].legend()
    axarr[1].plot(time,up,label='总点赞数')
    axarr[1].plot(time,comment,label='总评论数')
    plt.grid()
    plt.legend()
    plt.xlabel('日期')
    plt.show()

#词频图像
def key_():
    list=frequency_text('../other/data/key.csv')
    bardwidth=0.3
    xdata=[1,2,3,4,5,6,7,8,9,10]
    labels=[]
    ydata=[]
    num=1
    for line in list:
        labels.append(line[0])
        ydata.append(line[1])
        num=num+1
        if num>10:
            break
    print(ydata)
    plt.bar(xdata,ydata,bardwidth)
    plt.title('关键字词频分析')
    plt.ylabel('频率')
    plt.xticks(ticks=xdata,labels=labels)
    plt.legend()
    plt.grid()
    plt.show()

#情感分析图像
def emo_():
    list=emotion_text('../other/data/key.csv')
    list1=list[0]
    # list=[0.1,0.3,0.6]
    list_neg=list[1][0]
    list_pos=list[1][1]
    axes=['','','','']
    axes[0]=plt.subplot(211)
    axes[2]=plt.subplot(223)
    axes[3]=plt.subplot(224)

    print(type(axes[0]))
    for i in range(2):
        if i==1:
            list=list_neg
            title='负面词频'
        elif i==0:
            list=list_pos
            title='正面词频'
        print('list',list)
        bardwidth = 0.3
        xdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        labels = []
        ydata = []
        num = 1
        for line in list:
            labels.append(line[0])
            ydata.append(line[1])
            num = num + 1
            if num > 10:
                break
        print(ydata)
        print(type(axes[0]))
        axes[i+2].bar(xdata, ydata, bardwidth)
        axes[i+2].set_title(title)
        axes[i+2].set_ylabel('频率')
        axes[i+2].grid()
        axes[i+2].set_xticks(ticks=xdata, labels=labels)

    axes[0].set_title('关键词情感分析')
    axes[0].pie(list1,explode=(0.1,0.05,0),labels=['负面'+str(list1[0])[:5],'中性'+str(list1[1])[:5],'正面'+str(list1[2])[:5]],colors=['tomato', 'slategrey','dodgerblue'])
    plt.tight_layout()
    plt.show()

#分析热搜变化
def hot_():
    print("hot")
    hot_list=hot_band()
    change=[[],[],[],[]]
    title=[[],[],[],[]]
    degree=[[],[],[],[]]
    color = ['tomato', 'slategrey', 'dodgerblue']
    color_ = [[],[],[],[]]
    for i in range(0,4):
        print(i)
        hot_list[i].reverse()
        temp_color=[]
        for line in hot_list[i]:
            str_=str(line[3])
            if line[3]>=1:
                temp_color.append('tomato')
                print(1,end=' ')
            elif line[3]==-99:
                temp_color.append('lightgreen')
                print('new',end=' ')
                str_='new'
            elif line[3]<=-1 and hot_list[i][3]!=-99:
                temp_color.append('dodgerblue')
                print(-1,end=' ')
            elif line[3]==0:
                temp_color.append('slategrey')
                print(0,end=' ')
            else:
                print('error')

            title[i].append(line[0]+str_)
            degree[i].append(line[1])
        color_[i]=temp_color
        print(color_[i])

    fig,axxer=plt.subplots(1,4,figsize=(14,7))
    axxer=axxer.ravel()
    # for j in range(0,4):
    #     plt.title("第"+str(j+1)+"次热搜变化")
    #     plt.barh(range(len(title[j])),degree[j],height=0.3,color=color_[j])
    #     plt.yticks(range(len(degree[j])),title[j])
    #     plt.xlabel("热度")
    #     plt.ylabel("热搜")
    #     plt.grid(0.3)
    #     plt.show()
    for j in range(0,4):
        axxer[j].set_title("第"+str(j+1)+"次热搜变化")
        axxer[j].barh(range(len(title[j])),degree[j],height=0.5,color=color_[j])
        axxer[j].set_yticks(range(len(degree[j])),title[j])
        axxer[j].set_xlabel("热度")
        axxer[j].grid(0.3)
        axxer[j]
    plt.tight_layout()
    plt.show()
    # fig, axxer = plt.subplots(1, 2)
    # axxer = axxer.ravel()
    # for j in range(0,4):
    #     plt.title("第"+str(j+1)+"次热搜变化")
    #     plt.barh(range(len(title[j])),degree[j],height=0.3,color=color_[j])
    #     plt.yticks(range(len(degree[j])),title[j])
    #     plt.xlabel("热度")
    #     plt.ylabel("热搜")
    #     plt.grid(0.3)
    #     plt.show()
    # for j in range(2, 4):
    #     axxer[j-2].set_title("第" + str(j + 1) + "次热搜变化")
    #     axxer[j-2].barh(range(len(title[j])), degree[j], height=0.5, color=color_[j])
    #     axxer[j-2].set_yticks(range(len(degree[j])), title[j])
    #     axxer[j-2].set_xlabel("热度")
    #     axxer[j-2].grid(0.3)
    # plt.tight_layout()
    # plt.show()

if __name__ == '__main__':
    # user_()
    # key_()
    # emo_()
    # hot_()
    pass