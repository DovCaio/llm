if __name__ == "__main__": #Por conta do eval, que tem que importar isso daqui, isso dá problema, pois é invocado de um outro lugar
    import pipeline as pipeline
else:
    import src.pipeline as pipeline

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
import streamlit as st

class State(TypedDict):
    query: str
    docs: list
    response: str
    finded_docs: list
    feedback: str
    accept_sentences_or_not: str
    final_response: str


def retrive(state: State):
    docs = pipeline.retriever_agent(state["query"])
    return {"docs": docs}


def generate_text(state: State):
    print(state)
    if state.get("feedback"):
        responses = pipeline.response_with_quotes(f"{state["query"]} mas leve em consideração: {state['feedback']}", state["docs"])

    else: 
        responses = pipeline.response_with_quotes(state["query"], state["docs"])
    return {"response": responses[0], "finded_docs": responses[1]}


def feedback_and_self_check(state: State):
    check = pipeline.self_check(state["response"], state["finded_docs"])
    return {"accept_sentences_or_not": check, "feedback" : check}

def router(state: State):
    print(state["accept_sentences_or_not"])
    if "ESTÁ TUDO CERTO" in state["accept_sentences_or_not"]:
        return "ACEITO"
    return "Rejected + Feedback"

def safety_agent(state: State):
    safety = pipeline.safety_agent(state["response"])
    return {"final_response" : safety}



workflow = StateGraph(State)

workflow.add_node("retriver", retrive)
workflow.add_node("generate_text", generate_text)
workflow.add_node("feedback_and_self_check", feedback_and_self_check)
workflow.add_node("safety_agent", safety_agent)

workflow.add_edge(START, "retriver")
workflow.add_edge("retriver", "generate_text")
workflow.add_edge("generate_text", "feedback_and_self_check")
workflow.add_conditional_edges(
    "feedback_and_self_check",
    router,
    { 
        "ACEITO": "safety_agent",
        "Rejected + Feedback": "generate_text",
    },
)
workflow.add_edge("safety_agent", END)

optimizer_workflow = workflow.compile()

#state = optimizer_workflow.invoke({"query": "Quais são os direitos básicos de um cidadão?"})
#print(state["final_response"])

def interface():
    st.set_page_config(page_title="Chat Simples", page_icon="💬")

    st.title("💬 Chatbot para justiça social")

    # Guarda as mensagens no estado da sessão
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostra mensagens já enviadas
    for msg in st.session_state.messages:
        st.markdown(f"**{msg['user']}**: {msg['text']}")

    # Caixa de entrada
    user_input = st.text_input("Digite sua mensagem:")

    if st.button("Enviar"):
        if user_input.strip():
            # Adiciona mensagem do usuário
            st.session_state.messages.append({"user": "Você", "text": user_input})

            # Resposta simples (poderia ser um modelo, API etc.)
            state = optimizer_workflow.invoke({"query": user_input})
            resposta = state["final_response"]
            st.session_state.messages.append({"user": "Bot", "text": resposta})

            st.rerun()
    
    


if __name__ == "__main__":
    print("Executa a interface")
    interface()


