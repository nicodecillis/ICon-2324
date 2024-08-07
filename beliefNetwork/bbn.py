from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController


# costruzione della belief network
def build_network():
    # definizione delle variabili
    dev_already_popular = BbnNode(Variable(0, 'Disponibilità di app popolari già sul mercato',
                                           ['si', 'no']), [0.3, 0.7])
    brand_affiliation = BbnNode(Variable(1, 'Affiliazione ad un brand famoso', ['si', 'no']), [0.19, 0.81])
    dev_success = BbnNode(Variable(2, 'Successo dello sviluppatore',
                                   ['alto', 'basso']), [0.95, 0.05, 0.8, 0.2, 0.35, 0.65, 0.05, 0.95])
    ads = BbnNode(Variable(3, 'Pubblicità', ['si', 'no']), [0.2, 0.8])
    website = BbnNode(Variable(4, 'Sito web', ['si', 'no']), [0.1, 0.9])
    marketing = BbnNode(Variable(5, 'Marketing', ['ottimo', 'scarso']),
                        [0.97, 0.03, 0.8, 0.2, 0.22, 0.78, 0.02, 0.98])
    beta_testing = BbnNode(Variable(6, 'Beta testing', ['si', 'no']), [0.26, 0.74])
    price = BbnNode(Variable(7, 'Prezzo', ['gratis', 'a pagamento']), [0.88, 0.12])
    app_quality = BbnNode(Variable(8, 'Valore dell\'app', ['alto', 'basso']),
                          [0.98, 0.02, 0.76, 0.24, 0.82, 0.18, 0.64, 0.36, 0.73, 0.27, 0.29, 0.71, 0.47, 0.53,
                           0.14, 0.86, 0.82, 0.18, 0.46, 0.54, 0.67, 0.33, 0.35, 0.65, 0.62, 0.38, 0.12, 0.88, 0.41,
                           0.59, 0.04, 0.96])
    competition = BbnNode(Variable(9, 'Concorrenza', ['alta', 'bassa']), [0.78, 0.22])
    popularity = BbnNode(Variable(10, 'Popolarità', ['molto', 'poco']), [0.45, 0.55])
    market_state = BbnNode(Variable(11, 'Stato del mercato', ['emergente', 'saturato']),
                           [0.52, 0.48, 0.04, 0.96, 0.97, 0.03, 0.53, 0.47])
    app_success = BbnNode(Variable(12, 'Previsione del successo dell\'app non ancora sul mercato',
                                   ['alto', 'basso']), [0.98, 0.02, 0.77, 0.23, 0.34, 0.66, 0.03, 0.97])

    # definizione dei nodi e delle relazioni
    bbn = Bbn() \
        .add_node(dev_already_popular) \
        .add_node(brand_affiliation) \
        .add_node(dev_success) \
        .add_node(ads) \
        .add_node(website) \
        .add_node(marketing) \
        .add_node(beta_testing) \
        .add_node(price) \
        .add_node(app_quality) \
        .add_node(competition) \
        .add_node(popularity) \
        .add_node(market_state) \
        .add_node(app_success) \
        .add_edge(Edge(dev_already_popular, dev_success, EdgeType.DIRECTED)) \
        .add_edge(Edge(brand_affiliation, dev_success, EdgeType.DIRECTED)) \
        .add_edge(Edge(ads, marketing, EdgeType.DIRECTED)) \
        .add_edge(Edge(website, marketing, EdgeType.DIRECTED)) \
        .add_edge(Edge(beta_testing, app_quality, EdgeType.DIRECTED)) \
        .add_edge(Edge(dev_success, app_quality, EdgeType.DIRECTED)) \
        .add_edge(Edge(price, app_quality, EdgeType.DIRECTED)) \
        .add_edge(Edge(marketing, app_quality, EdgeType.DIRECTED)) \
        .add_edge(Edge(competition, market_state, EdgeType.DIRECTED)) \
        .add_edge(Edge(popularity, market_state, EdgeType.DIRECTED)) \
        .add_edge(Edge(app_quality, app_success, EdgeType.DIRECTED)) \
        .add_edge(Edge(market_state, app_success, EdgeType.DIRECTED))
    return bbn


def add_value_to_node(tree, node_name, answer, value):
    ev = EvidenceBuilder() \
        .with_node(tree.get_bbn_node_by_name(node_name)) \
        .with_evidence(answer, value) \
        .build()
    tree.set_observation(ev)


def collect_observations(tree):
    while True:
        value = input("Hai già app di successo sul mercato?\n"
                      "Risposte possibili: si / no\n").lower()
        if value in ['si', 'no']:
            add_value_to_node(tree, 'Disponibilità di app popolari già sul mercato', value, 1)
            break
        else:
            print("Input non valido. Riprova.")

    while True:
        value = input("Sei affiliato ad un brand famoso?\n"
                      "Risposte possibili: si / no\n").lower()
        if value in ['si', 'no']:
            add_value_to_node(tree, 'Affiliazione ad un brand famoso', value, 1)
            break
        else:
            print("Input non valido. Riprova.")

    while True:
        value = input("La tua app ha previsto una fase di beta testing?\n"
                      "Risposte possibili: si / no\n").lower()
        if value in ['si', 'no']:
            add_value_to_node(tree, 'Beta testing', value, 1)
            break
        else:
            print("Input non valido. Riprova.")

    while True:
        value = input("La tua app è gratis o a pagamento?\n"
                      "Risposte possibili: gratis / a pagamento\n").lower()
        if value in ['gratis', 'a pagamento']:
            add_value_to_node(tree, 'Prezzo', value, 1)
            break
        else:
            print("Input non valido. Riprova.")

    while True:
        value = input("La tua app ha un sito web associato?\n"
                      "Risposte possibili: si / no\n").lower()
        if value in ['si', 'no']:
            add_value_to_node(tree, 'Sito web', value, 1)
            break
        else:
            print("Input non valido. Riprova.")

    while True:
        value = input("Hai investito in pubblicità per la tua app?\n"
                      "Risposte possibili: si / no\n").lower()
        if value in ['si', 'no']:
            add_value_to_node(tree, 'Pubblicità', value, 1)
            break
        else:
            print("Input non valido. Riprova.")

    while True:
        value = input("La concorrenza nella categoria associata alla tua app è alta o bassa?\n"
                      "Risposte possibili: alta / bassa\n").lower()
        if value in ['alta', 'bassa']:
            add_value_to_node(tree, 'Concorrenza', value, 1)
            break
        else:
            print("Input non valido. Riprova.")

    while True:
        value = input("Quanto è popolare la categoria associata alla tua app?\n"
                      "Risposte possibili: molto / poco\n").lower()
        if value in ['molto', 'poco']:
            add_value_to_node(tree, 'Popolarità', value, 1)
            break
        else:
            print("Input non valido. Riprova.")

    prediction(tree)


def prediction(tree):
    belief = tree.get_posteriors()
    for node, posteriors in belief.items():
        if node == "Previsione del successo dell'app non ancora sul mercato":
            max, min = posteriors.items()
            print("La probabilità di successo dell'app è pari a " + str(round(max[1] * 100, 1)) + "%")
            if max[1] < 0.3:
                print("Probabilità di successo bassa.\nContinua a migliorare e a credere nella tua visione, "
                      "perché anche i più grandi successi sono partiti da sfide enormi.")
            elif max[1] < 0.4:
                print("Probabilità di successo medio-bassa.\nLa tua app ha già una buona base di partenza. Ogni passo "
                      "avanti è un'opportunità per apprendere e crescere.\nCon dedizione e determinazione, puoi "
                      "trasformare il potenziale della tua app in un successo concreto.")
            elif max[1] < 0.5:
                print("Probabilità di successo media.\nSei sulla strada giusta!\nCon ulteriori perfezionamenti e "
                      "maggior impegno, puoi fare la differenza e raggiungere livelli di successo ancora più alti.")
            elif max[1] < 0.7:
                print(
                    "Probabilità di successo medio-alta.\nContinua a lavorare sodo e a perfezionare ogni aspetto della "
                    "tua app.\nSei a un passo dal trasformare la tua app in un vero successo!")
            else:
                print("Probabilità di successo alta.\nOttimo lavoro! Le probabilità di successo della tua app sono "
                      "eccellenti.\nMantieni questo ritmo e continua a innovare; il successo è dietro l'angolo e il "
                      "tuo impegno sarà sicuramente ricompensato.")
