import json
import requests, os
import threading
from multiprocessing.dummy import Pool as ThreadPool

base = 'https://unsplash.com/napi/search/photos?query={}&xp=&per_page=20&page={}'

last = 1
keywords = ['bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
            'fire hydrant',
            'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
            'zebra',
            'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
            'sports ball', 'kite',
            'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
            'fork', 'knife',
            'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut',
            'cake',
            'chair', 'sofa', 'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor',
            'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
            'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
            ]
max_num = 36


def getdata(a, url):
    headers = {
        'Referer': 'https://unsplash.com/s/photos/{}'.format(a),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.106 Safari/537.36 '
    }
    global last
    # 9651
    try:
        response = requests.get(url, headers=headers)
        arr = json.loads(response.text)
        if last == 1:
            last = arr['total_pages']
            if last > max_num:
                last = max_num
        return arr['results']
    except Exception:
        return []


def download(id):
    # print(id)
    a = id[0]
    #print(a)
    id = id[1]
    url = 'https://unsplash.com/photos/{}/download?force=true&w=640'.format(id)
    headers = {
        'Referer': 'https://unsplash.com/s/photos/{}'.format(a),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.106 Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    img = response.content
    # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
    if not os.path.exists('./pic/{}/'.format(a)):
        try:
            os.mkdir('./pic/{}/'.format(a))
        except Exception:
            pass
    with open('./pic/{}/{}.jpg'.format(a, id), 'wb') as f:
        f.write(img)
        f.flush()
        f.close()
    print(a+': ./pic/{}/{}.jpg'.format(a, id))


# 多线程
def start_thread_save_img(img_list):
    # 方式一：使用线程池
    pool = ThreadPool(6)
    pool.map(download, img_list)
    pool.close()
    # pool.join()  # join所完成的工作就是线程同步，即主线程任务结束之后，进入阻塞状态，一直等待其他的子线程执行结束之后，主线程在终止

    # 方式二：没有线程限制
    # for url in img_url_list:
    #     th = threading.Thread(target=save_img, args=(url,))
    #     th.start()


for a in keywords:
    print('Here:' + a)
    data = getdata(a, base.format(a, 1))
    arr = []
    for index in data:
        # download(i['id'])
        arr.append([a, index['id']])
    start_thread_save_img(arr)

    for i in range(2, last + 1):
        print('now is: ' + str(i))
        data = getdata(a, base.format(a, i))
        # print(data)
        arr = []
        for index in data:
            # download(i['id'])
            arr.append([a, index['id']])
        start_thread_save_img(arr)