# -*- coding: utf-8 -*-
"""FP KLASIFIKASI ISPU.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14gWpUaAphwr3eES9SZGi7DKF7jG9Gg3g

# FINAL PROJECT DATA MINING

> ## Kelas Data Mining B
> #### - Rendi Panca Wijanarko (21082010016)
> #### - Maulana Bryan Syahputra (210820038)
> #### - Syauqillah Hadie Ahsana (21082010042)

# EDA (Exploratory Data Analysis)
"""

# Import library untuk analisis data
import numpy as np
import pandas as pd

# Import library untuk visualisasi data
import seaborn as sns
import matplotlib.pyplot as plt

# Import Data
df = pd.read_csv ('https://raw.githubusercontent.com/syha-studio/FinalProjectDataMining/refs/heads/main/Indeks%20Standar%20Pencemaran%20Udara%20(ISPU)%20Tahun%202021%20-%202022.xlsx%20-%20Fixed%20Data.csv')

df.head()

df.shape

df.dtypes

df.describe()

df.isnull().sum()

df['Category'].unique()

"""## Delete Attribute Periode Data, Tanggal, Stasiun, Critical"""

df = df.drop(columns=['Periode Data','Tanggal','Stasiun','MAX','Critical'])

df.head(3)

"""## Delete Row dengan Kategori "TIDAK ADA DATA"
"""

df = df[df['Category'] != "TIDAK ADA DATA"]

df['Category'].unique()

"""## Handling Missing Value"""

df.isnull().sum()

df = df.dropna(subset=['Category'])

df.isnull().sum()

# Using Imputation According to Category
df['PM10'] = df.groupby('Category')['PM10'].transform(lambda x: x.fillna(x.median()))
df['PM2,5'] = df.groupby('Category')['PM2,5'].transform(lambda x: x.fillna(x.median()))
df['SO2'] = df.groupby('Category')['SO2'].transform(lambda x: x.fillna(x.median()))
df['CO'] = df.groupby('Category')['CO'].transform(lambda x: x.fillna(x.median()))
df['O3'] = df.groupby('Category')['O3'].transform(lambda x: x.fillna(x.median()))
df['NO2'] = df.groupby('Category')['NO2'].transform(lambda x: x.fillna(x.median()))

df.isnull().sum()

"""## Detecting and Handling Outlier"""

# detecting using boxplot (seaborn)
columns = [col for col in df.columns if col != 'Category']
n = len(columns)
rows = (n + 1) // 2

plt.figure(figsize=(12, rows * 2))
for i, column in enumerate(columns, 1):
    plt.subplot(rows, 2, i)
    sns.boxplot(data=df, x=column)
    plt.title(f'Boxplot of {column}')
    plt.tight_layout()

# Show the plot
plt.show()

"""> #### Tidak Perlu Handling Outliers Karena Data Outliers Masuk Akal

## DATA TRANSFORMATION
"""

Category = {"TIDAK SEHAT":1, "SEDANG":2, "BAIK":3}
df["Category"]=df["Category"].map(Category)

"""## Feature Selection"""

def ISPU_Correlation(df):
    correlation = df.corr()
    sns.heatmap(correlation, annot=True, cbar=True, cmap="RdYlGn")

data_numerik = df.select_dtypes(include=['float64', 'int64'])
ISPU_Correlation(data_numerik)

"""> #### Dari Grafik Korelasi, semua atribut memiliki korelasi tinggi terhadap Category. Oleh karena itu semua atribut akan digunakan untuk membuat model klasifikasi

# Pembuatan Model Klasifikasi

### Algoritma yang digunakan
> #### Decision Tree
> > **Alasan:** Decision Tree bisa memberikan hasil yang baik dengan dataset ukuran ini dan memberikan visualisasi yang jelas tentang keputusan yang diambil.
> #### Random Forest
> > **Alasan:** Dibandingkan Decision Tree tunggal, Random Forest lebih tahan terhadap overfitting karena menggabungkan hasil dari banyak pohon (ensemble).
"""

# Import Library Algorithm
from sklearn.model_selection import train_test_split
# Import Algorithm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# Import Evaluation Model
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix
# ROC AUC
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt
plt.rc("font", size=14)
# import Crossval
from sklearn.model_selection import cross_val_score

X = df[['PM10', 'PM2,5', 'SO2', 'CO', 'O3','NO2']]
y = df['Category']

"""## Skenario Perbandingan 70% -30%"""

# Splitting the data into training and testing sets (70% training, 30% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=27)

"""### Decission Tree Algorithm"""

# Initializing the Decision Tree model
clf=DecisionTreeClassifier()
# Fitting the model on the training data
clf=clf.fit(X_train,y_train)
# Making predictions on the test data
y_pred=clf.predict(X_test)
# Evaluating the model
conf_matrix = confusion_matrix(y_test, y_pred)
# Outputting the results
print('Confusion Matrix:')
print(conf_matrix)
print('--------------')
print('Classification Report:')
print(classification_report(y_test, y_pred))

"""### Random Forest"""

# Initializing the RandomForest
modelfix = RandomForestClassifier()
# Fitting the model on the training data
modelfix = modelfix.fit(X_train, y_train)
# Making predictions on the test data
y_pred = modelfix.predict(X_test)
# Evaluating the model
conf_matrix = confusion_matrix(y_test, y_pred)
# Outputting the results
print('Confusion Matrix:')
print(conf_matrix)
print('--------------')
print('Classification Report:')
print(classification_report(y_test, y_pred))

"""## Evaluasi Model Klasifikasi Skenario Perbandingan 70% -30%

> ### HOLD - OUT
"""

# Menghitung ROC-AUC untuk model Decision Tree
dt_roc_auc = roc_auc_score(y_test, clf.predict_proba(X_test), multi_class='ovr', average='macro')

# Membuat ROC curve untuk Decision Tree
dt_fpr, dt_tpr, _ = roc_curve(y_test, clf.predict_proba(X_test)[:, 1], pos_label=clf.classes_[1])

# Menghitung ROC-AUC untuk model Random Forest
rf_roc_auc = roc_auc_score(y_test, modelfix.predict_proba(X_test), multi_class='ovr', average='macro')

# Membuat ROC curve untuk Random Forest
rf_fpr, rf_tpr, _ = roc_curve(y_test, modelfix.predict_proba(X_test)[:, 1], pos_label=modelfix.classes_[1])

# Plotting ROC curve untuk Decision Tree dan Random Forest
plt.figure()
plt.plot(dt_fpr, dt_tpr, color='red', label=f'DT (AUC = {dt_roc_auc:.2f})')
plt.plot(rf_fpr, rf_tpr, color='green', label=f'RF (AUC = {rf_roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')  # Plot diagonal garis referensi
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve DT vs RF')
plt.legend(loc='lower right')
plt.show()

"""> ### CROSS-VAL

> > ###  Decision Tree
"""

scores_accuracy = cross_val_score(clf, X, y, cv=5, scoring="accuracy")
print(scores_accuracy)
scores_precission = cross_val_score(clf, X, y, cv=5, scoring="precision_macro")
print(scores_precission)
scores_recall = cross_val_score(clf, X, y, cv=5, scoring="recall_macro")
print(scores_recall)
scores_f1 = cross_val_score(clf, X, y, cv=5, scoring="f1_macro")
print(scores_f1)

print("Rata-rata Nilai Akurasi: %0.2f (+/- %0.2f)" % (scores_accuracy.mean(), scores_accuracy.std()))
print("Rata-rata Nilai Precision Macro: %0.2f (+/- %0.2f)" % (scores_precission.mean(), scores_precission.std()))
print("Rata-rata Nilai Recall Macro: %0.2f (+/- %0.2f)" % (scores_recall.mean(), scores_recall.std()))
print("Rata-rata Nilai F1 Macro: %0.2f (+/- %0.2f)" % (scores_f1.mean(), scores_f1.std()))

"""> > ###  Random Forest"""

scores_accuracy = cross_val_score(modelfix, X, y, cv=5, scoring="accuracy")
print(scores_accuracy)
scores_precission = cross_val_score(modelfix, X, y, cv=5, scoring="precision_macro")
print(scores_precission)
scores_recall = cross_val_score(modelfix, X, y, cv=5, scoring="recall_macro")
print(scores_recall)
scores_f1 = cross_val_score(modelfix, X, y, cv=5, scoring="f1_macro")
print(scores_f1)

print("Rata-rata Nilai Akurasi: %0.2f (+/- %0.2f)" % (scores_accuracy.mean(), scores_accuracy.std()))
print("Rata-rata Nilai Precision Macro: %0.2f (+/- %0.2f)" % (scores_precission.mean(), scores_precission.std()))
print("Rata-rata Nilai Recall Macro: %0.2f (+/- %0.2f)" % (scores_recall.mean(), scores_recall.std()))
print("Rata-rata Nilai F1 Macro: %0.2f (+/- %0.2f)" % (scores_f1.mean(), scores_f1.std()))

"""## Skenario Perbandingan 60% - 40%"""

# Splitting the data into training and testing sets (60% training, 40% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=27)

"""### Decission Tree Algorithm"""

# Initializing the Decision Tree model
clf=DecisionTreeClassifier()
# Fitting the model on the training data
clf=clf.fit(X_train,y_train)
# Making predictions on the test data
y_pred=clf.predict(X_test)
# Evaluating the model
conf_matrix = confusion_matrix(y_test, y_pred)
# Outputting the results
print('Confusion Matrix:')
print(conf_matrix)
print('--------------')
print('Classification Report:')
print(classification_report(y_test, y_pred))

"""### Random Forest"""

# Initializing the RandomForest
model = RandomForestClassifier()
# Fitting the model on the training data
model = model.fit(X_train, y_train)
# Making predictions on the test data
y_pred = model.predict(X_test)
# Evaluating the model
conf_matrix = confusion_matrix(y_test, y_pred)
# Outputting the results
print('Confusion Matrix:')
print(conf_matrix)
print('--------------')
print('Classification Report:')
print(classification_report(y_test, y_pred))

"""## Evaluasi Model Klasifikasi Skenario Perbandingan 60% -40%

> ### HOLD - OUT
"""

# Menghitung ROC-AUC untuk model Decision Tree
dt_roc_auc = roc_auc_score(y_test, clf.predict_proba(X_test), multi_class='ovr', average='macro')

# Membuat ROC curve untuk Decision Tree
dt_fpr, dt_tpr, _ = roc_curve(y_test, clf.predict_proba(X_test)[:, 1], pos_label=clf.classes_[1])

# Menghitung ROC-AUC untuk model Random Forest
rf_roc_auc = roc_auc_score(y_test, model.predict_proba(X_test), multi_class='ovr', average='macro')

# Membuat ROC curve untuk Random Forest
rf_fpr, rf_tpr, _ = roc_curve(y_test, model.predict_proba(X_test)[:, 1], pos_label=model.classes_[1])

# Plotting ROC curve untuk Decision Tree dan Random Forest
plt.figure()
plt.plot(dt_fpr, dt_tpr, color='red', label=f'DT (AUC = {dt_roc_auc:.2f})')
plt.plot(rf_fpr, rf_tpr, color='green', label=f'RF (AUC = {rf_roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')  # Plot diagonal garis referensi
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve DT vs RF')
plt.legend(loc='lower right')
plt.show()

"""> ### CROSS-VAL

> > ###  Decision Tree
"""

scores_accuracy = cross_val_score(clf, X, y, cv=5, scoring="accuracy")
print(scores_accuracy)
scores_precission = cross_val_score(clf, X, y, cv=5, scoring="precision_macro")
print(scores_precission)
scores_recall = cross_val_score(clf, X, y, cv=5, scoring="recall_macro")
print(scores_recall)
scores_f1 = cross_val_score(clf, X, y, cv=5, scoring="f1_macro")
print(scores_f1)

print("Rata-rata Nilai Akurasi: %0.2f (+/- %0.2f)" % (scores_accuracy.mean(), scores_accuracy.std()))
print("Rata-rata Nilai Precision Macro: %0.2f (+/- %0.2f)" % (scores_precission.mean(), scores_precission.std()))
print("Rata-rata Nilai Recall Macro: %0.2f (+/- %0.2f)" % (scores_recall.mean(), scores_recall.std()))
print("Rata-rata Nilai F1 Macro: %0.2f (+/- %0.2f)" % (scores_f1.mean(), scores_f1.std()))

"""> > ###  Random Forest"""

scores_accuracy = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print(scores_accuracy)
scores_precission = cross_val_score(model, X, y, cv=5, scoring="precision_macro")
print(scores_precission)
scores_recall = cross_val_score(model, X, y, cv=5, scoring="recall_macro")
print(scores_recall)
scores_f1 = cross_val_score(model, X, y, cv=5, scoring="f1_macro")
print(scores_f1)

print("Rata-rata Nilai Akurasi: %0.2f (+/- %0.2f)" % (scores_accuracy.mean(), scores_accuracy.std()))
print("Rata-rata Nilai Precision Macro: %0.2f (+/- %0.2f)" % (scores_precission.mean(), scores_precission.std()))
print("Rata-rata Nilai Recall Macro: %0.2f (+/- %0.2f)" % (scores_recall.mean(), scores_recall.std()))
print("Rata-rata Nilai F1 Macro: %0.2f (+/- %0.2f)" % (scores_f1.mean(), scores_f1.std()))

"""# MODEL TERBAIK UNTUK DEPLOYMENT

# TERPILIH : RANDOM FOREST (70-30)
"""