# Churn Intelligence
**Hack4Her · Arca Continental · Tec de Monterrey**

Sistema de predicción de riesgo de churn para el canal tradicional de Arca Continental. Identifica qué clientes están en riesgo de dejar de comprar antes de que ocurra y activa automáticamente un protocolo de retención.

---

## Stack

- Python 3.13 · scikit-learn · imbalanced-learn
- MongoDB Atlas
- ElevenLabs
- Streamlit · Plotly

---

## Estructura

```
hackathon-churn/
├── data/
│   ├── sales_churn_train.csv
│   ├── sales_churn_test.csv
│   ├── Clientes.csv
│   ├── Coolers.csv
│   ├── preds_submission.csv
│   ├── preds_submission_final.csv
│   ├── llamada_alto.mp3
│   └── llamada_medio.mp3
├── model/
│   ├── model.pkl
│   └── label_encoder.pkl
├── assets/
│   └── arcacontinental.png
├── exploracion.ipynb
├── dashboard.py
└── README.md
```

---

## Instalación

```bash
pip install pandas scikit-learn imbalanced-learn pymongo \
            elevenlabs streamlit plotly certifi requests
```

---

## Reproducción paso a paso

### 1. Entrenar el modelo y generar predicciones

Abrir y ejecutar `exploracion.ipynb` de arriba a abajo. El notebook está dividido en 8 secciones:

1. Imports
2. Carga de datos
3. Análisis exploratorio (EDA)
4. Ingeniería de features
5. Modelo — Random Forest + SMOTE
6. Predicciones sobre el set de prueba
7. Guardar modelo
8. MongoDB + ElevenLabs

Al finalizar se generan:
- `model/model.pkl`
- `model/label_encoder.pkl`
- `data/preds_submission_final.csv`
- `data/llamada_alto.mp3`
- `data/llamada_medio.mp3`

### 2. Correr el dashboard

```bash
cd hackathon-churn
streamlit run dashboard.py
```

Abrir en el navegador: `http://localhost:8501`

---

## Resultados del modelo

| Métrica | Valor |
|---------|-------|
| AUC | 0.9987 |
| Precision (churn) | 0.72 |
| Recall (churn) | 0.99 |
| Clientes en riesgo alto | 2,519 |

---

## Hallazgos clave

1. **Caída de cajas** — los clientes en churn caen 22 cajas en promedio el mes previo a abandonar
2. **Hogares** — subcanal con mayor churn (3.4%) — 3.5x el promedio
3. **Clientes Mini** — 3.5% de churn vs 0.03% en clientes Gigante
4. **Territorio** — impacto mínimo (0.01%). El riesgo es transversal
5. **Coolers** — correlación de -0.02. No protegen si las compras caen

---

## Variables del modelo

| Variable | Importancia |
|----------|-------------|
| uni_boxes_sold_m | 43.3% |
| promedio_cajas | 24.5% |
| num_transacciones | 23.6% |
| cajas_por_puerta | 6.0% |
| size_enc | 1.9% |
| num_coolers | 0.5% |

---

**Hack4Her 2026 · Tec de Monterrey · Arca Continental**
