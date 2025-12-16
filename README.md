# The_Guardian_Grid
Sistema inteligente que utiliza Topologia Elétrica para agrupar chamados, transformar listas de sintomas em diagnósticos de infraestrutura e blindar a operação contra desperdícios.

# [cite_start]⚡ O Guardião: Inteligência Operacional via Topologia de Redes 

## [cite_start]1. O Problema: o Custo da Operação [cite: 2]

Atualmente, a operação funciona baseada em uma "lista de chamados", ou seja, "um para um". [cite_start]Se entram 10 reclamações sobre a falta de luz para a mesma rua, o sistema tende a interpretar que existem 10 chamados diferentes que precisam ser abertos e resolvidos. [cite: 3]

> *Como indivíduo, presenciei um episódio onde essa dinâmica ficou escancarada na minha frente, pois, dois postes estavam com as chaves fusíveis abertas, e ao abrir o chamado para a empresa, o movimento em resposta foi o envio de uma equipe de técnicos para fiscalizar o porquê minha residência estava sem luz. [cite_start]Nesse caso em específico, a operação se preocupou com o sintoma individual (o cliente), enquanto o fusível da esquina estava queimado (a causa generalizada).* [cite: 3, 4]

Para a gestão de **WFM** (workforce management), isso é um pesadelo: consumimos horas produtivas da equipe, gastamos combustível e deixamos a rede desligada por mais tempo, tudo porque o sistema olhou para o "micro" (o cliente) e ignorou o "macro" (a rede). [cite: 5, 6]

* [cite_start]**O Cenário:** Quando múltiplos clientes de uma mesma rua ficam sem energia (um fusível queimado, por exemplo), o sistema atual tende a tratar cada reclamação como uma ordem de serviço isolada. [cite: 7]
* [cite_start]**A Consequência:** O WFM gera ordens de "verificação de cliente", enviando equipes para olhar medidores individuais, quando o defeito real está no equipamento de média e/ou baixa tensão. [cite: 8]
* [cite_start]**O Custo:** Isso infla o **OPEX** com deslocamentos improdutivos, aumenta o **TMA** (Tempo Médio de Atendimento) e expõe a equipe a riscos desnecessários, enquanto o defeito real na rede continua ativo. [cite: 9]

---

## [cite_start]2. Metodologia e Desafio: o mapeamento em Grafos [cite: 10]

Um dos maiores entraves dentro dessa operacionalização é que o sistema legado enxerga as reclamações como "lista de compras", ou itens soltos que precisam de atenção individual. Portanto, o desafio técnico não está na operacionalização do atendimento, mas sim na inteligência de conectar um problema semelhante a outro. [cite_start]O desafio, portanto, é a **lógica de agrupamento**. [cite: 11, 12, 13]

Precisamos de uma camada de inteligência que consiga "segurar" a ansiedade do sistema de despachar imediatamente. [cite_start]Ao invés disso, é necessário que sejamos capazes de ter previsibilidade em **geolocalização topológica**. [cite: 14, 15]

> **Exemplo:** Eu posso ser vizinho de muro do João, mas meu fio vem do poste da esquerda e o dele, do poste da direita. Se o meu poste queima, eu fico sem energia, mas o João continua com luz. Eles são vizinhos geográficos, mas **estranhos topológicos**. [cite_start]O desafio não é apenas coletar os dados, mas entender a relação entre eles. [cite: 16, 17, 18, 19]

[cite_start]Para que seja possível mapear as "zonas de interferência", podemos nos guiar por perguntas simples mas com grandes potenciais: [cite: 20]
1.  [cite_start]Das 10 pessoas que ligaram, quantas são alimentadas pelo mesmo Transformador? [cite: 21]
2.  [cite_start]Estatisticamente, se 5 vizinhos caíram, qual é a probabilidade do defeito estar no fusível da esquina e não nas casas? [cite: 22]
3.  [cite_start]Se o padrão se repete em ruas paralelas, estamos lidando com um problema de Média Tensão (bairro) ou Baixa Tensão (rua)? [cite: 23]

[cite_start]**O grande desafio técnico é que nossos sistemas legados enxergam "listas" (tabelas SQL), mas a eletricidade flui em "redes" (grafos).** [cite: 24]

* [cite_start]**A Metodologia:** Adotamos uma abordagem de *Domain-Driven Design (DDD)* aliada à **Teoria dos Grafos**. [cite: 26]
* **A Mudança de Paradigma:** Em vez de analisar quem está reclamando (o CPF), analisamos onde ele está conectado na árvore genealógica da rede. [cite_start]Qual Transformador é o "pai" dessa Unidade Consumidora? [cite: 27, 28]
* [cite_start]**O Diferencial:** Criar uma camada lógica intermediária que intercepta os chamados antes de virarem Ordem de Serviço, aplicando algoritmos de **Clusterização Espacial**. [cite: 29]

---

## [cite_start]3. Construtos da Solução (O MVP) [cite: 30]

> [cite_start]*"Simples, Escalável e Orientado a Eventos."* [cite: 31]

[cite_start]A proposta que traçamos para interceptar os chamados feitos em filas "um por um", é acionar um sistema de algoritmo que vá tratar os chamados como "agrupamento de incidentes". [cite: 32]

[cite_start]Denominamos a proposta como **"O Guardião"**, que refere-se a um sistema automatizado que atua como um filtro inteligente e preditivo antes da Ordem de Serviço ser criada. [cite: 33]

A proposta é ser simples, escalável e orientado a eventos reais utilizando a lógica de topologia (quem está ligado em quem), o algoritmo analisa o padrão das reclamações em tempo real. [cite_start]Se ele detecta que um grupo de chamados pertence ao mesmo transformador, ele **bloqueia o envio de equipes para as casas** e gera um único alerta prioritário para o equipamento da rede. [cite: 34, 35]

> [cite_start]*É sair do modelo de "atender cliente por cliente" para o modelo de "restaurar o bloco inteiro" com uma única manobra.* [cite: 36]

[cite_start]A solução proposta é um microsserviço preditivo estruturado em três pilares: [cite: 37]

### 3.1. [cite_start]O Mapa Virtual (Digital Twin) [cite: 38]
Em um primeiro momento, nos preocupamos com a estruturação em JSON onde o nó conhece seus dependentes. Dessa forma, podemos nos atentar à modelagem da rede elétrica como um **Grafo Direcionado (Directed Graph)**. [cite_start]O sistema mapeia a hierarquia energética, estabelecendo relações claras de dependência (*quem alimenta quem*) entre Subestações, Transformadores e Unidades Consumidoras. [cite: 39, 40, 41]

### 3.2. [cite_start]O Motor de Decisão (Core Logic) [cite: 42]
[cite_start]Para conseguirmos um resultado otimizado, é preciso seguir uma **regra de ouro**: se mais de três residências da mesma rua abrem chamados, a necessidade de atendimento não é individual, mas sim, **estrutural e sistêmica**. [cite: 43]

[cite_start]Para que isso seja realizado de forma eficiente, é necessário usar o algoritmo de inferência desenvolvido em **Python + NetworkX**, integrado ao barramento de eventos (**Kafka**). [cite: 44]

* **Lógica de Agrupamento:** O sistema monitora a densidade de incidentes em janelas de tempo curtas (< 10 min). [cite_start]Se múltiplos pontos (clientes) reportam falha simultânea, o algoritmo identifica o **Problema Comum** mais provável (transformador) como a causa-raiz. [cite: 45, 46]

### 3.3. [cite_start]A Saída Otimizada (Output) [cite: 47]
[cite_start]Para que tenhamos um output significativo, precisamos entender que as múltiplas ordens de serviço fragmentadas precisam ser realocadas para uma única OS agrupada — **Parent Order**. [cite: 48]

[cite_start]O despacho é redirecionado automaticamente para o **Ativo de Rede** (causa), eliminando visitas improdutivas às residências (sintoma) e otimizando a rota da equipe. [cite: 49]

Dessa forma, com a substituição da pulverização de chamados por um **Despacho Centralizado**, o algoritmo identifica que o defeito é na rede, ele bloqueia o envio de equipes para as casas individualmente e gera uma única ordem de serviço para o equipamento defeituoso. [cite_start]O resultado é uma rota única e assertiva, sem desperdício de tempo e combustível. [cite: 50, 51]
