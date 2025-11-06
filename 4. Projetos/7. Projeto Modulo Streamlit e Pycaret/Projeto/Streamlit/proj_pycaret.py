import streamlit as st
import pandas as pd
import time 
from pycaret.classification import *
from pycaret.utils.generic import check_metric
import os


st.title("🤖 Estudo dos Dados por Pycaret")

st.header("Utilize o pycaret para pre processar os dados e rodar o modelo lightgbm. ")

st.markdown('''
---
Para entendimento desse código utilizarei as biblitecas mencionadas a seguir''')
 
st.code(''' 
from pycaret.classification import *
from pycaret.utils.generic import check_metric
''', language = "python")

st.markdown('''
e para estudo da base em pycaret,o código desenvolvido foi:
''')

st.code(''' 
def model_pycaret(data, resposta, data_unseen=None):
    
    tm_inicio = time.time()
    
    print("Análise inicial dos dados da base:")
    exp_clf101 = setup(data=data, target=resposta, session_id=123)
    
    print("Comparando os resultados dos modelos:")
    try:
        fold_input = input("📊 Quantos folds você deseja usar na validação cruzada? (pressione Enter para usar 10): ")
        fold_num = int(fold_input) if fold_input.strip() != "" else 10
    except ValueError:
        fold_num = 10
        print("⚠️ Valor inválido, usando padrão: 10 folds")
    
    compare_models(fold=fold_num, sort="AUC")
    results = pull()
    print("\nMétricas dos modelos apurados: ")
    display(results)

    print("Modelos disponíveis:")
    print(results.index.to_list())
    
    model = input("👉 Digite o nome do modelo que deseja usar (ou pressione Enter para usar o melhor modelo automaticamente): ")
    if model.strip() == "":
        model = results.index[0]
        print(f"🔹 Nenhum modelo informado. Usando o melhor modelo: {model}")
    else:
        if model not in results.index:
            print(f"⚠️ Modelo '{model}' não encontrado. Usando o melhor modelo automaticamente: {results.index[0]}")
            model = results.index[0]
        else:
            print(f"🔹 Modelo escolhido manualmente: {model}")

    # Criando e desenvolvendo o modelo
    bm = create_model(model)
    tun = tune_model(bm, optimize='F1')
    
    # Diagnostic print (remove after testing)
    print(f"Model type: {type(tun)}")
    print(f"Has predict_proba? {hasattr(tun, 'predict_proba')}")

    # Visualização do modelo (com checks para plots que precisam de proba)
    if hasattr(tun, 'predict_proba'):
        plot_model(tun, plot='auc')
        plot_model(tun, plot='pr')
    else:
        print("⚠️ Skipping AUC and PR plots: Model does not support probability predictions.")
    
    plot_model(tun, plot='feature')  # Não precisa de proba
    plot_model(tun, plot='confusion_matrix')  # Não precisa de proba

    print("Avaliando o modelo:")
    evaluate_model(tun)
    predict_model(tun)
    print("Resultado antes da finalização do modelo:")
    print(tun)
    
    final = finalize_model(tun)
    print("Resultado do modelo finalizado:")
    print(final)
    
    print("Dados do melhor modelo encontrado depois da modelagem: ", final)

    # Bloco pro data_unseen
    if data_unseen is not None:
        print("Fazendo previsões no conjunto não utilizado ainda")
        unseen_predictions = predict_model(final, data=data_unseen)
        
        true_labels = unseen_predictions[resposta].astype(str)
        pred_labels = unseen_predictions['prediction_label'].astype(str)  # PyCaret 3.x naming
        
        acc = check_metric(true_labels, pred_labels, metric='Accuracy')
        print(f"Acurácia do modelo final ({resposta}): {acc}")
    else:
        print("Nenhum dataset 'data_unseen' fornecido para teste.")
    
    tm_fim = time.time()
    print(f"Tempo total de execução: {tm_fim - tm_inicio:.2f} segundos")
    
    return {"modelo final": final, "metricas": results}
''', language = "python")

st.markdown('''Para análise do desenvolvimento e tempo do código será possível escolher o tamanho da amostra e comparar com os resultados da base inteira.
''')
st.markdown("## Resultado utilizando o sample da base de dados:")
##########################################################
# Código
df = pd.read_feather('credit_scoring.ftr')
smp = st.slider("Sample",
        max_value = 750000 - 1, 
        min_value = 1,
        value= 750000 - 1 )
dt = df.sample(smp)

dt.drop(['data_ref','index'], axis=1, inplace=True)
data = dt.sample(frac=0.95, random_state=786)
data_unseen = dt.drop(data.index)


data.reset_index(inplace=True, drop=True)
data_unseen.reset_index(inplace=True, drop=True)

def model_pycaret(data, resposta, data_unseen=None, run_name="run1"):
    st.subheader(f"🚀 Treinamento de Modelo com PyCaret — {run_name}")

    tm_inicio = time.time()

    # --- Setup ---
    with st.spinner("Configurando ambiente do PyCaret..."):
        exp_clf101 = setup(data=data, target=resposta, session_id=123, html=False)
    st.success("✅ Setup concluído com sucesso!")

    # --- Seleção do número de folds ---
    fold_num = st.number_input(
        "📊 Quantos folds você deseja usar na validação cruzada:",
        min_value=2,
        max_value=20,
        value=10,
        step=1,
        key=f"fold_input_pycaret_{run_name}"
    )

    # --- Comparação de modelos ---
    st.write("🔍 Comparando os resultados dos modelos...")
    with st.spinner("Comparando modelos..."):
        compare_models(fold=fold_num, sort="AUC")
        results = pull()

    st.write("### 📈 Métricas dos Modelos")
    st.dataframe(results, use_container_width=True)

    # --- Escolha do modelo ---
    model_choices = results.index.to_list()
    model = st.selectbox(
        "👉 Escolha o modelo que deseja usar (ou deixe o primeiro para o melhor automaticamente):",
        options=model_choices,
        index=0,
        key=f"select_model_pycaret_{run_name}"
    )

    # --- Criação e ajuste do modelo ---
    st.write(f"🔧 Treinando e ajustando o modelo **{model}**...")
    with st.spinner("Treinando o modelo..."):
        bm = create_model(model)
        tun = tune_model(bm, optimize='F1')

    # --- Avaliação Visual do Modelo ---
    st.write("## 📊 Avaliação Visual do Modelo")

    def show_plot(fig):
        """Detecta o tipo de gráfico e exibe no Streamlit"""
        if fig is None:
            st.warning("⚠️ Gráfico não disponível para este modelo.")
        elif "plotly" in str(type(fig)).lower():
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.pyplot(fig, use_container_width=True)

    if hasattr(tun, 'predict_proba'):
        st.write("### Curva ROC / AUC")
        fig_auc = plot_model(tun, plot='auc', display_format='streamlit', save=False)
        show_plot(fig_auc)

        st.write("### Precision-Recall Curve")
        fig_pr = plot_model(tun, plot='pr', display_format='streamlit', save=False)
        show_plot(fig_pr)
    else:
        st.warning("⚠️ Gráficos AUC e PR não disponíveis — o modelo não suporta probabilidade.")

    st.write("### Importância das Variáveis")
    fig_feat = plot_model(tun, plot='feature', display_format='streamlit', save=False)
    show_plot(fig_feat)

    st.write("### Matriz de Confusão")
    fig_cm = plot_model(tun, plot='confusion_matrix', display_format='streamlit', save=False)
    show_plot(fig_cm)

    # --- Avaliação final ---
    st.write("Avaliando o modelo:")
    evaluate_model(tun)
    predict_model(tun)
    st.write("Resultado antes da finalização do modelo:")
    results_tuned = pull()
    st.dataframe(results_tuned, use_container_width=True)
    
    final = finalize_model(tun)
    st.write("Resultado do modelo finalizado:")
    results_final = pull()
    st.dataframe(results_final, use_container_width=True)

    # --- Predição em dados não vistos ---
    if data_unseen is not None:
        st.write("### 🔍 Avaliando o modelo com dados não vistos")
        unseen_predictions = predict_model(final, data=data_unseen)
        result_unseen = pull() 
        st.dataframe(result_unseen, use_container_width=True)

        true_labels = unseen_predictions[resposta].astype(str)
        pred_labels = unseen_predictions['prediction_label'].astype(str)
        acc = check_metric(true_labels, pred_labels, metric='Accuracy')

        st.info(f"Acurácia no conjunto: {acc:.3f}")
    else:
        st.info("⚠️ Nenhum conjunto 'data_unseen' foi fornecido.")

    tm_fim = time.time()
    st.write(f"⏱️ **Tempo total de execução:** {tm_fim - tm_inicio:.2f} segundos")

    return {"modelo_final": final, "metricas": results}
##########################################################
result_sample = model_pycaret(dt, 'mau', data_unseen, run_name=f"base_sample_{smp}")
pycaret_model_sample = result_sample["modelo_final"]

st.markdown("## Download do modelo treinado usando sample da base do Pycaret")

pycaret_sample = save_model(pycaret_model_sample,f'Final Model Pycaret Project Sample {smp}')

if isinstance(pycaret_sample, tuple):
    pycaret_sample_path = pycaret_sample[1]  
else:
    pycaret_sample_path = pycaret_sample     

if not pycaret_sample_path.endswith(".pkl"):
    pycaret_sample_path = f"{pycaret_sample_path}.pkl"


with open(pycaret_sample_path, "rb") as f:
    sample_model_bytes = f.read()

st.download_button(
    label="📥 Download",
    data = sample_model_bytes, 
    file_name = f"Final Model Pycaret Project Sample {smp}.plk",
    mime="application/octet-stream")

st.markdown("## Resultado utilizando a base de dados completa:")

df.drop(['data_ref','index'], axis=1, inplace=True)
data_df = df.sample(frac=0.95, random_state=786)
data_test = df.drop(data_df.index)

result_full = model_pycaret(df, 'mau', data_test, run_name="base_completa")
pycaret_model_full = result_full["modelo_final"]


st.markdown("## Download do modelo treinado usando da base inteira do Pycaret")

pycaret_full = save_model(pycaret_model_full,f'Final Model Pycaret Project Full')

if isinstance(pycaret_full, tuple):
    pycaret_full_path = pycaret_full[1]  .pkl
else:
    pycaret_full_path = pycaret_full     

if not pycaret_full_path.endswith(".pkl"):
    pycaret_full_path = f"{pycaret_full_path}.pkl"

with open(pycaret_full_path, "rb") as f:
    model_bytes = f.read()

st.download_button(
    label="📥 Download",
    data = pycaret_bytes, 
    file_name = f"Final Model Pycaret Project.plk",
    mime="application/octet-stream")


st.markdown('''Percebeu-se uma mudança nos modelos de melhor desempenho conforme o tamanho da base de dados utilizada. O modelo Linear Kernel apresentou melhor performance na base com recorte (sample), enquanto o Gradient Boosting Classifier (GBC) obteve melhor desempenho na base completa. Isso pode ter ocorrido por alguns motivos: (i) a base inteira possui maior variabilidade entre os dados e suas interações, tornando a análise menos linear; (ii) o GBC tende a aproveitar melhor grandes volumes de dados para aprendizado; (iii) esse modelo é mais propenso ao overfitting em bases mais genéricas; e (iv) a base original apresenta desbalanceamento entre as classes de “mau pagador”.
Como exemplo podemos comparar as duas fontes de dados, com a mesma quantidade de folds (sendo uma com um sample de 37500, e outra com a fonte de dados completa) e a análise dos respectivos modelos de melhor desempnheo temos os seguintes dados resultates, como esperado, o modelo treinado com a base completa apresentou melhor resultado preditivo, com aumento de acurácia de 0,11, aproximadamente. No entanto, houve também um aumento de 3690% no tempo de processamento. Dessa forma, considerando o contexto desta análise e o recorte utilizado para a amostra, pode-se concluir que o uso da base completa, embora mais preciso, torna-se moroso e pesado, sendo recomendado apenas em casos em que ganhos preditivos justificam o custo computacional.''')