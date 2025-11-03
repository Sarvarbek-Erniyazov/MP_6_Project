# 📊 JUP Coin Multi-Class Classification Loyihasi Xulosasi

Ushbu loyiha **JUP** kriptovalyutasining kelgusi **1 soatlik narx harakatini** **Multi-Class Classification** (Ko'p Sinfli Tasniflash) usullari yordamida bashorat qilishga qaratilgan bo'lib, natijada **Buy, Sell, Hold** savdo qarorlarini qo'llab-quvvatlovchi mashinaviy o'rganish (ML) modeli yaratildi.

---

## 1. Ma'lumot Yig'ish (Web Scraping) Jarayoni 🌐

* **Ma'lumot Manbai:** Binance API (so'nggi **365 kunlik**, 1 soatlik OHLCV ma'lumotlari).
* **Qamrab olingan Aktivlar:** APE, ARB, FIL, GALA, **JUP**, OP, SEI, TIA (**8 ta** aktiv).
* **Interval:** `1h`.

---

## 2. Loyihaning Maqsadi va JUP Tanlovi 🎯

### Maqsad
Kriptobozor tebranishlaridan foydalanib, **Buy, Sell, Hold** strategiyalarini avtomatlashtirish uchun ishonchli ML modeli yaratish.

### Nima uchun aynan JUP?
JUP coinining 8 ta aktiv ichida **eng yuqori soatlik tebranishga ($\sigma$)** ega bo'lganligi sababli tanlab olindi, chunki bu model uchun eng kuchli bashoratlash signali hisoblanadi.

| Coin | Std Dev ($\sigma$) | Izoh |
| :--- | :---: | :--- |
| FIL | 0.010329 | Eng past |
| **JUP** | **0.013045** | **Eng yuqori tebranish (Optimal Signal)** |
| TIA | 0.012841 | Yuqori, ammo JUP dan past |

---

## 3. Multi-Class Target Yaratish (`JUP_Target_MultiClass`) 🧮

Kelajakdagi 1 soatlik narx o'zgarishi $\pm 0.3\%$ chegarasi asosida **3 ta sinfga** ajratildi:

### Target Sinfining Tashkil Etilishi

$$
\text{JUP\_Future\_Return} = \frac{\text{JUP\_Close}_{(t+1)} - \text{JUP\_Close}_{(t)}}{\text{JUP\_Close}_{(t)}}
$$

* **0 (Down):** Agar Return $< -0.003$ (ya'ni, $-0.3\%$ dan ko'p tushsa)
* **1 (Sideways):** Agar $-0.003 \le \text{Return} \le +0.003$ (**Minority Class**)
* **2 (Up):** Agar Return $> +0.003$ (ya'ni, $+0.3\%$ dan ko'p ko'tarilsa)

---

## 4. Feature Engineering (Texnik Ko'rsatkichlar Yaratish) ⚙️

Modelni o'qitish uchun **13 ta** turli xil xususiyatlar (feature) yaratildi, jumladan:

* **Volatillik/Rentabellik:** Logarifmik rentabellik, 5 va 20 soatlik volatilnost.
* **Trend/Momentum:** 10 va 50 soatlik SMA, **14 soatlik RSI**.
* **Vaqt Xususiyatlari:** `FE_Hour`, `FE_DayOfWeek`.

> **Yakuniy Natija:** $\sim 100k$ kuzatuvga ega bo'lgan **`data/multi_class_JUP_engineered_features.csv`** fayli hosil bo'ldi.

---

## 5. Model Training va Multi-Class Classification Natijalari 🤖

Asosiy baholash mezonlari: **Accuracy** va **F1-macro**.

### 📊 5.1 Modellar Taqqoslash (Ma'lumotlar Muvozanatlangan Holatda)

| Dataset | Model | Accuracy | F1\_macro | F1\_Class\_1 (Sideways) |
| :--- | :--- | :---: | :---: | :---: |
| Imbalanced | Gradient Boosting | 0.397 | 0.366 | 0.230 |
| **Balanced** | **Random Forest** | **0.432** | **0.427** | **0.544** |
| Balanced | Gradient Boosting | 0.380 | 0.374 | 0.331 |

### 🏆 5.2 Eng Yaxshi Modelni Aniqlash

**Eng yaxshi model:** **Balanced Random Forest**

* **Accuracy:** 0.432
* **F1\_macro:** 0.427
* **F1\_Class\_1 (Sideways, eng kichik sinf):** **0.544**

### ⚖️ 5.3 SMOTE (Data Balancing) Tahlili Samaradorligi

Ma'lumotlarni muvozanatlashtirish (**SMOTE** bilan) natijalarini sezilarli darajada yaxshiladi:

| Model | F1\_macro Imbalanced | F1\_macro Balanced | O'zgarish | F1\_Class\_1 Balanced | O'zgarish |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Random Forest | 0.367 | **0.427** | **+0.060** | **0.544** | **+0.291** |

---

## 6. Model Tuning Natijalari va Xulosalar 🏁

### Model Tuning Jadvali (Random Forest)

| Rank | Tuning Metodi | Test F1 Macro | Test Accuracy | Eng Muvofiq Parametrlar | Vaqt (s) |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **1** | **Bayesian Optimization** | **0.4310** | 0.4336 | `n_estimators: 300, max_depth: 26, criterion: entropy` | 81.12 |
| 2 | Manual Fine-Tune | 0.4242 | 0.4267 | `n_estimators: 200, max_depth: 25, ...` | 24.46 |
| 3 | Random Search | 0.4226 | 0.4238 | ... | 33.25 |

### Chuqur Tahlil va Talqin 🔍

* **Asosiy Muammo:** Eng yuqori **F1 Macro** ko'rsatkichi ($\sim 0.43$) hali ham moliyaviy vaqt qatorlari uchun **past** hisoblanadi.
* **Sabab:** Hozirgi **13 ta feature** (xususiyat) murakkab narx dinamikasini to'liq qamrab olish uchun **yetarli emas**.

### Modelni Yaxshilash Strategiyasi 🚀

Modelning bashorat kuchini oshirish uchun keyingi qadamlar belgilandi:

1.  **Feature Engineering (Asosiy Prioritet):**
    * Qo'shimcha **volatillik** (masalan, ATR) va **momentum** (masalan, MACD, Stochastic Oscillator) indikatorlarini qo'shish.
    * **Lagged Feature’lar** (maqsad o'zgaruvchining oldingi qiymatlari) kiritish.
    * Feature Selection (RFE yoki Permutation Importance) orqali eng muhimlarini tanlash.
2.  **Model Arxitekturasi:**
    * Random Forest baseline natijalari maksimal darajada yaxshilandi. Endi kuchliroq **ensemble algoritmlarini** sinash kerak: **XGBoost, LightGBM, CatBoost**.
3.  **Yakuniy Tuning:**
    * Yangi, boyitilgan feature to'plami bilan **Bayesian Optimization** yoki **Optuna** yordamida yangi parametrlar optimallashtiriladi.

---

Ushbu loyiha **Random Forest** modelining **Bayesian Optimization** yordamida **Test F1 Macro: 0.4310** ga erishganini ko'rsatdi. Keyingi qadamlar **feature engineering** va **kuchliroq GBM/LGBM modellarini** sinashga qaratilgan.

---

Keyingi qadam sifatida, sizga JUP uchun yangi, boyitilgan xususiyatlar (masalan, ATR, MACD va 5 ta lag qiymatlari) bilan **XGBoost** modelini o'qitish va natijalarni taqqoslashda yordam berishim mumkinmi?
