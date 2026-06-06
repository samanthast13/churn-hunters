# Churn Hunters — Hack4Her · Arca Continental

Solución de predicción de churn para el canal tradicional de Arca Continental.

## Problema
Arca Continental pierde $12MM MXN mensuales en clientes que dejan de comprar sin detección temprana.

## Solución
Sistema de scoring de riesgo usando Random Forest entrenado con datos reales de ventas, clientes y coolers.

## Resultados
- AUC: 0.9987
- 2,535 clientes identificados en riesgo
- 2,519 en riesgo alto

## Variables más importantes
1. uni_boxes_sold_m (43%)
2. promedio_cajas (24%)
3. num_transacciones (23%)

## Respuestas a las 3 preguntas
1. Las variables de volumen de compra (cajas vendidas y transacciones) son las más predictivas
2. El territorio tiene impacto mínimo (0.01%) en el churn
3. Los coolers tienen bajo impacto directo (0.46%) — el comportamiento de compra es más determinante

## Archivos
- `exploracion.ipynb` — EDA, features, modelo y predicciones
- `data/preds_submission_final.csv` — predicciones finales

## Stack
- Python, scikit-learn, pandas, imbalanced-learn
- Random Forest + SMOTE para desbalance
