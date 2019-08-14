from math import sqrt


class Constants:

    sequence = [
        ['L', 'N', 'N', 'L', 'H', 'N', 'N', 'N', 'N', 'N', 'N', 'H'],
        ['N', 'H', 'L', 'L', 'L', 'N', 'L', 'N', 'L', 'N', 'N', 'L'],
        ['H', 'L', 'H', 'N', 'N', 'L', 'H', 'N', 'L', 'L', 'L', 'N'],
    ]

    A = [
        [0.6, 0.2, 0.2],
        [0.01, 0.8, 0.19],
        [0.01, 0.09, 0.9],
    ]

    B = [
        [0.1, 0.5, 0.4],
        [0.3, 0.4, 0.3],
        [0.8, 0.19, 0.01],
    ]

    pi = [1 / 3, 1 / 3, 1 / 3]

    evidence_probab = {
        "N": [0.1, 0.3, 0.8],
        "L": [0.5, 0.4, 0.19],
        "H": [0.4, 0.3, 0.01],
    }


def solve():
    exploration_transitions = []
    maintenace_transitions = []
    forgetting_transitions = []
    for row_index, row in enumerate(Constants.A):
        for elem_index, trans_pred in enumerate(row):
            print(trans_pred)
            if elem_index == 0:
                exploration_transitions.append(trans_pred)
            if elem_index == 1:
                maintenace_transitions.append(trans_pred)
            if elem_index == 2:
                forgetting_transitions.append(trans_pred)
    trans_prob = exploration_transitions, maintenace_transitions, forgetting_transitions
    return trans_prob


def forward(trans_prob, multipliers, friends):
    print()
    day_prediction = prediction_without_evidence(trans_prob, multipliers)
    day_prediction_with_evidence = prediction_with_evidence(day_prediction, friends)
    print("day_prediction", day_prediction)
    print("day_prediction_with_evidence", day_prediction_with_evidence)
    if Constants.sequence[friends]:
        forward(trans_prob, day_prediction_with_evidence, friends)
    else:
        print(day_prediction_with_evidence)
        return day_prediction_with_evidence


def prediction_without_evidence(trans_probabilities, multipliers):
    sums = [0, 0, 0]
    for column in trans_probabilities:
            for i, mult in enumerate(multipliers):
                sums[i] += column[i] * mult
    return sums


def prediction_with_evidence(day_prediction, friends):
    evidence = Constants.sequence[friends].pop(0)
    print(evidence)
    evidence_prob = Constants.evidence_probab[evidence]
    print(evidence_prob)
    updated_probabilities = [0, 0, 0]
    normalized_prob = [0, 0, 0]

    for i in range(len(evidence_prob)):
        updated_evidence_prob = evidence_prob[i] * day_prediction[i]
        updated_probabilities[i] = updated_evidence_prob
    denominator = updated_probabilities[0] + updated_probabilities[1] + updated_probabilities[2]
    for i in range(len(evidence_prob)):
        normalized_prob[i] = updated_probabilities[i] / denominator
    print(normalized_prob)
    return normalized_prob


forward(solve(), Constants.pi, 0)

