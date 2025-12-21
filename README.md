```mermaid

graph TD
    subgraph "🐍 SEUS SCRIPTS PYTHON (No Host)"
        style Gerador fill:#f9f,stroke:#333,stroke-width:2px,color:black
        style Arquivista fill:#f9f,stroke:#333,stroke-width:2px,color:black
        style Oraculo fill:#d4a5ff,stroke:#333,stroke-width:2px,color:black,font-weight:bold
        
        Gerador[⚡ Gerador de Caos<br/>Generating...]
        Arquivista[💾 Agente Arquivista<br/>Saving...]
        Oraculo[🧙‍♂️ Oráculo Topológico<br/>Plotting...]
        Tela{{📈 Gráfico Matplotlib<br/>Espaço de Fase}}
    end

    subgraph "🐳 INFRA DOCKER (Guardian Grid)"
        style Kafka fill:#ccf,stroke:#333,stroke-width:2px,color:black
        style Mongo fill:#ff9,stroke:#333,stroke-width:2px,color:black
        
        Kafka(🚚 KAFKA BROKER<br/>Porta: 9092)
        Mongo[(🗄️ MONGODB<br/>Porta: 27017)]
        
        subgraph "Suporte"
            style Zookeeper fill:#eee,stroke:none
            style Kafdrop fill:#eee,stroke:none
            Zookeeper(👮‍♂️ Zookeeper) -.- Kafka
            Kafdrop(📺 Kafdrop UI) -.- Kafka
        end
    end

    %% O CAMINHO DO DADO
    Gerador == "1. Envia JSON" ==> Kafka
    Kafka == "2. Consome Tópico" ==> Arquivista
    Arquivista == "3. Grava Histórico" ==> Mongo
    Mongo -. "4. Lê Janela de Tempo" .-> Oraculo
    ´´´
    Oraculo == "5. Renderiza" ==> Tela
