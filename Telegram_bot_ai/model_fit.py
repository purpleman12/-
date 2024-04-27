import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

# тестовые данные для выборки
ingredients = [
    ["Водка", "Тоник", "Клубничный сироп"],
    ["Ром", "Лимон", "Сахар"],
    ["Джин", "Тоник", "Лайм"],
    ["Текила", "Сок апельсина", "Гренадин"],
    ["Виски", "Содовая", "Лимон"],
    ["Ликер", "Сливки", "Кофейный ликер"],
    ["Вермут", "Лед", "Оливка"],
    ["Сок лимона", "Сахарный сироп", "Лед"],
    ["Сок лайма", "Сахар", "Мята"],
    ["Сок апельсина", "Лед", "Клубничный сироп"],
    ["Гренадин", "Лимон", "Водка"],
    ["Сахарный сироп", "Мятные листья", "Ром"],
    ["Содовая", "Лимон", "Виски"],
    ["Тоник", "Лайм", "Джин"],
    ["Клубничный сироп", "Лед", "Водка"],
    ["Мятные листья", "Лимон", "Ром"],
    ["Персиковый сироп", "Апельсин", "Ром"],
    ["Кокосовое молоко", "Банан", "Ром"],
    ["Кофейный ликер", "Водка", "Лед"],
    ["Ирландский крем", "Виски", "Лед"],
    ["Молоко", "Шоколад", "Ликер"],
    ["Сливки", "Шоколад", "Ликер"],
    ["Яичный желток", "Сахар", "Виски"],
    ["Какао", "Молоко", "Ликер"],
    ["Ананасовый сок", "Ром", "Лайм"],
    ["Клубничный сироп", "Ром", "Клубничный ликер"],
    ["Кокосовый крем", "Ром", "Кокосовый ром"],
    ["Банан", "Ром", "Кокосовое молоко"],
    ["Маракуйя", "Ром", "Кокосовое молоко"],
    ["Мандариновый сок", "Ром", "Апельсиновый ликер"]
]
cocktails = [
    "Маргарита", "Мохито", "Дайкири", "Текила санрайз", "Манихаттен",
    "Пина колада", "Мартини", "Мохито", "Секс на пляже", "Пина колада",
    "Космополитен", "Белый русский", "Эгг-ног", "Пина колада", "Даикери",
    "Май тай", "Маргарита", "Пина колада", "Белый русский", "Ирландский кофе",
    "Эгг-ног", "Белый русский", "Ирландский кофе", "Эгг-ног", "Пина колада",
    "Маргарита", "Пина колада", "Пина колада", "Пина колада"
]
# Токенизация ингредиентов
tokenizer = Tokenizer(num_words=1000, oov_token="<OOV>")
tokenizer.fit_on_texts(ingredients)
print("fit_texts: ",tokenizer)
sequences = tokenizer.texts_to_sequences(ingredients)
print("sequences: ",sequences)

padded_sequences = pad_sequences(sequences, padding='post')
print("padded_sequences: ",padded_sequences)

# Кодирование названий коктейлей
label_encoder = LabelEncoder()

labels = label_encoder.fit_transform(cocktails)
print("label_encoder.fit_transform(cocktails): ",labels)
labels = to_categorical(labels)
print("to_categorical(labels):",labels)
#Создание модели
model = Sequential([
    Embedding(input_dim=1000, output_dim=16, input_length=padded_sequences.shape[1]),
    LSTM(128),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(labels.shape[1], activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# Обучение модели
model.fit(padded_sequences, labels, epochs=10, validation_split=0.2)
#оценка модели
loss, accuracy = model.evaluate(padded_sequences, labels)
print(f'Accuracy: {accuracy*100:.2f}%')
max_len = 20
def predict_function(new_ingredients_mes,tokenizer, model, label_encoder,max_len):
    new_ingredients = [new_ingredients_mes]

    # Токенизация новых ингредиентов
    new_sequences = tokenizer.texts_to_sequences(new_ingredients)
    new_padded_sequences = pad_sequences(new_sequences, padding='post', maxlen=max_len)

    # Предсказание
    predictions = model.predict(new_padded_sequences)

    # Преобразование предсказаний в исходные названия коктейлей
    predicted_cocktails = label_encoder.inverse_transform(predictions.argmax(axis=1))
    max_len = 20
    # Вывод предсказанных коктейлей
    for i in range(len(new_ingredients)):
        print(f"Ingredients: {new_ingredients[i]} - Predicted Cocktail: {predicted_cocktails[i]}")
    return predicted_cocktails[0]
for i in range(5):
    test = input()
    print(predict_function(test,tokenizer, model, label_encoder,max_len))