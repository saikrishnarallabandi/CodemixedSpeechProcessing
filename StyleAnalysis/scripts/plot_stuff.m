spanish = load('spanish_spans.txt')
spanish_nonzero = spanish(spanish > 0)
histogram(spanish_nonzero,'Normalization','probability')

