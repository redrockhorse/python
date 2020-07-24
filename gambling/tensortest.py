__author__ = 'mahy'
import tensorflow as tf
import numpy as np

# a = np.random.random((5, 1))
# b = np.random.randint(0, 9, (7, 5))
# bais = np.random.randint(0, 9, (5, 1))
# c = tf.tensordot(b.astype(np.float), a.astype(np.float), axes=1)
# print(a)
# print('--------------------------------------')
# print(b)
# # print(bais)
# print('--------------------------------------')
# print(c.numpy())


# d = tf.add(c, bais)
# print(d.numpy())

'''
class LinearLayer(tf.keras.layers.Layer):
    def __init__(self, units):
        super().__init__()
        self.units = units

    def build(self, input_shape):
        # w参数张量,实现矩阵乘法只需要获取输入张量最后一个维度的长度,即input_shape[-1]
        self.w = self.add_weight(name='w',
                                 shape=[input_shape[-1], self.units], initializer=tf.zeros_initializer())
        # b从参数张量,形状为units,执行张量加法时可通过broadcast自动扩展
        self.b = self.add_weight(name='b',
                                 shape=[self.units], initializer=tf.zeros_initializer())

    def call(self, inputs):
        # y=wx+b
        y_pred = tf.matmul(inputs, self.w) + self.b
        return y_pred


class LinearModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.layer = LinearLayer(units=1)

    def call(self, inputs):
        output = self.layer(inputs)
        return output


class MeanSquaredError(tf.keras.losses.Loss):
    def call(self, y_true, y_pred):
        return tf.reduce_mean(tf.square(y_pred - y_true))


class SparseCategoricalAccuracy(tf.keras.metrics.Metric):
    def __init__(self):
        super().__init__()
        self.total = self.add_weight(name='total', dtype=tf.int32, initializer=tf.zeros_initializer())
        self.count = self.add_weight(name='count', dtype=tf.int32, initializer=tf.zeros_initializer())

    def update_state(self, y_true, y_pred, sample_weight=None):
        values = tf.cast(tf.equal(y_true, tf.argmax(y_pred, axis=-1, output_type=tf.int32)), tf.int32)
        self.total.assign_add(tf.shape(y_true)[0])  # assign_add 对应元素相加
        self.count.assign_add(tf.reduce_sum(values))

    def result(self):
        return self.count / self.total


# layer = LinearLayer(1)
# layer.build(input_shape=[None, 64*6])
# model = LinearModel()
# model.add(layer)
# model.build(input_shape=[None, 64*6])
# model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
#               loss=MeanSquaredError(),
#               metrics=[SparseCategoricalAccuracy()])


"""顺序模型：类似于搭积木一样一层、一层放上去"""
# model = tf.keras.Sequential()
"""添加层:其实就是 wx+b"""
# model.add(tf.keras.layers.Dense(32, input_shape=(7, 7),activation='relu'))
'''

# inputs = tf.keras.Input(shape=(7,7), name='digits')
class MyLayer(tf.keras.layers.Layer):
    def __init__(self, unit=49):
        super(MyLayer, self).__init__()
        self.unit = unit

    def build(self, input_shape):
        self.weight = self.add_weight(shape=(7*7,7),
                                      initializer=tf.keras.initializers.RandomNormal(),
                                      trainable=True)
        self.bias = self.add_weight(shape=(7),
                                    initializer=tf.keras.initializers.Zeros(),
                                    trainable=True)

    def call(self, inputs):
        return tf.matmul(inputs, self.weight) + self.bias


class myModel(tf.keras.Model):

    def __init__(self):
        # 调用母类中的__init__()方法
        super(myModel, self).__init__()
        # 调用自定义层类 并构建每一层的连接数
        self.fc1 = MyLayer(49)
        self.fc2 = tf.keras.layers.Dense(7)


    # 构建一个五层的全连接网络
    def call(self, inputs, training=None):
        inputs = tf.reshape(inputs, [-1, 7*7])
        # 把训练数据输入到自定义层中
        x = self.fc1(inputs)
        # 利用relu函数进行非线性激活操作
        out = tf.nn.relu(x)
        x = self.fc2(out)
        return x


netWork = myModel()
netWork.build(input_shape=[None,7*7])
netWork.summary()

# netWork.compile(optimizer=optimizers.Adam(lr=1e-3),
#                 loss=tf.losses.CategoricalCrossentropy(from_logits=True),
#                 metrics=['accuracy']
#                 )
# netWork.fit(db_train, epochs=10, validation_data=db_test,
#             validation_freq=2
#             )
# netWork.evaluate(db_test)



'''
my_layer = MyLayer(7)
x = np.random.random((7, 7))
out = my_layer(x)
print(x)
print('===========')
print(out)
inputs = MyLayer(7)
h1 = tf.keras.layers.Dense(7, activation='relu')(inputs)
outputs = tf.keras.layers.Dense(7, activation='softmax')(h1)
model = tf.keras.Model(inputs, outputs)
model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss=tf.keras.losses.categorical_crossentropy,
               metrics=[tf.keras.metrics.categorical_accuracy])
'''



import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
cursor_lt = conn.cursor()

sql = "select *  from jc.td_ptl_ssq_data where pdate>'2018-02-27'  order by pdate asc"
cursor.execute(sql)
result = cursor.fetchall()
rs = []
data = []
for row in result:
    item = []
    rowdata = np.zeros(64)
    item.append(int(row['v1']))
    item.append(int(row['v2']))
    item.append(int(row['v3']))
    item.append(int(row['v4']))
    item.append(int(row['v5']))
    item.append(int(row['v6']))
    item.append(int(row['v7']))
    data.append(item)
#print(data)
train_x = []
train_y = []
start = 0
end = 7
n = len(data)
while end < n:
    train_x.append(data[start:end])
    train_y.append(data[end])
    start += 1
    end += 1
print(train_x[327])
print(train_y[0])
train_x = np.array(train_x,dtype=float)
train_y = np.array(train_y,dtype=float)

# inputs = tf.keras.Input(shape=(7,7), name='mnist_input')
# h1 = tf.keras.layers.Dense(7, activation='relu')(inputs)
# # h1 = tf.keras.layers.Dense(64, activation='relu')(h1)
# outputs = tf.keras.layers.Dense(7, activation='softmax')(h1)
# model = tf.keras.Model(inputs, outputs)
# model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss=tf.keras.losses.categorical_crossentropy,
#                metrics=[tf.keras.metrics.categorical_accuracy])
# model.fit(train_x, train_y, batch_size=7, epochs=57, validation_split=0.1)


xlen = len(train_x)
netWork.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss=tf.keras.losses.categorical_crossentropy)
print(train_x.shape)
print(train_y.shape)
history = netWork.fit(train_x.reshape(xlen,49), train_y, steps_per_epoch=1, epochs=57, validation_split=0.1)
print(history.history['loss'][-1])
end_loss = history.history['loss'][-1]
# while end_loss > 200:
#     history = netWork.fit(train_x.reshape(xlen, 49), train_y, steps_per_epoch=5, epochs=757, validation_split=0.1)
#     end_loss = history.history['loss'][-1]
print(data[-7:])
predictions = netWork.predict(np.array(data[-7:],dtype=float).reshape(1,49))
print(predictions)