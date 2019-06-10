import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from get_data import Get_data
import one_hot_services
import jieba_services
import mongoDB_services

def padding(data_list, value = 0, maxlen = 50):
    data = keras.preprocessing.sequence.pad_sequences(
        data_list, value=value, padding='post', maxlen=maxlen
    )
    return data

def cnn_model(vocab_size = 20000, embedding_size = 200, sequence_length = 50):
    model = keras.Sequential()
    model.add(layers.Embedding(input_dim = vocab_size, output_dim = embedding_size, input_length = sequence_length))
    model.add(layers.Conv1D(filters = embedding_size, kernel_size = 3, strides = 1, padding = 'valid'))
    model.add(layers.MaxPool1D(2, padding = 'valid'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation = 'relu'))
    model.add(layers.Dense(1, activation = 'sigmoid'))
    return model

def lstm_model(vocab_size = 20000, embedding_size = 200, sequence_length = 50):
    model = keras.Sequential()
    model.add(layers.Embedding(input_dim = vocab_size, output_dim = embedding_size, input_length = sequence_length))
    model.add(layers.LSTM(64, return_sequences = True))
    model.add(layers.LSTM(1, activation = 'sigmoid', return_sequences = False))
    return model

def conv_layers(embedding_size = 200, sequence_length = 50, kernels = [3, 4, 5]):
    input_layer = layers.Input(shape = (sequence_length, embedding_size, 1))
    cnns = []
    for i in kernels:
        conv = layers.Conv2D(filters = embedding_size, kernel_size = (i, embedding_size), strides = 1, padding = 'valid', activation = 'relu')(input_layer)
        pool = layers.MaxPool2D(pool_size = (sequence_length - i + 1, 1), padding = 'valid')(conv)
        cnns.append(pool)
    output_layer = layers.concatenate(cnns)
    model = keras.Model(inputs = input_layer, outputs = output_layer)
    return model

def multi_cnn(vocab_size = 20000, embedding_size = 200, sequence_length = 50, kernels = [3, 4, 5]):
    model = keras.Sequential()
    model.add(layers.Embedding(input_dim = vocab_size, output_dim = embedding_size, input_length = sequence_length))
    model.add(layers.Reshape((sequence_length, embedding_size, 1)))
    model.add(conv_layers(embedding_size = embedding_size, sequence_length = sequence_length, kernels = kernels))
    model.add(layers.Flatten())
    model.add(layers.Dense(200, activation = 'relu'))
    model.add(layers.Dense(1, activation = 'sigmoid'))
    return model

def early_stop(patience = 1):
    callbacks = [
        keras.callbacks.EarlyStopping(
            # Stop training when `val_loss` is no longer improving
            monitor='loss',
            # "no longer improving" being defined as "no better than 1e-2 less"
            min_delta=1e-2,
            # "no longer improving" being further defined as "for at least 2 epochs"
            patience=patience,
            verbose=1
        )
    ]
    return callbacks

if __name__ == '__main__':
    G = Get_data()
    collections = G.get_data(1000)
    _collections = [[jieba_services.cut_sentence(i[0], 'list'), i[1]] for i in collections]
    corpus = []
    for i in _collections:
        corpus.extend(i[0])
    word_ids = one_hot_services.make_dict(corpus)

    x_ = [one_hot_services.word2id(i[0], word_ids) for i in _collections]
    y_ = [i[1] for i in _collections]

    x_train = padding(x_[200:])
    x_test = padding(x_[:1000-200])
    y_train = y_[200:]
    y_test = y_[:1000-200]

    vocab_size = 200000
    # model = keras.Sequential()
    # model.add(layers.Embedding(vocab_size, 200))
    # model.add(layers.GlobalAveragePooling1D())
    # model.add(layers.Dense(64, activation='relu'))
    # model.add(layers.Dense(1, activation='sigmoid'))
    # model.summary()
    callbacks = early_stop()
    # model = cnn_model(vocab_size = vocab_size)
    model = multi_cnn(vocab_size = vocab_size)
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train,
                        epochs=4,
                        verbose=1, batch_size = 64, callbacks = callbacks)

    result = model.evaluate(x_test, y_test)
    print(result)