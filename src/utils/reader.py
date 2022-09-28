from time import time
from typing import Tuple
import json 
import numpy as np 
import pdb 
class Reader:
    def __init__(self, file):
        self.file = file

    def read(self):
        raise NotImplementedError

class TopLogitFormatSequenceReader(Reader):

    def read(self) -> Tuple[np.array]:
        all_top_preds = []
        all_is_correct = []
        with open(self.file, 'r') as f:
            for line in f:
                line = json.loads(line)
                top_k_logits = np.array(line['top_logits'])
                top_k_logit_idxs = np.array(line['top_logit_idxs'])
                # get the top 1 logit and idx
                top_one_logit_local_idx = np.argmax(top_k_logits, axis=-1)
                seq_len = top_one_logit_local_idx.shape

                if len(seq_len) > 1: 
                    # TODO: implement batched version
                    raise NotImplementedError(f"Currently batched outputs are not supported.\
                         Try generating outputs a single example at a time.")

                seq_len = seq_len[0]

                # get the actual single top logit, not assuming they're sorted already 
                top_one_logit_local_idx = top_one_logit_local_idx.reshape((seq_len, 1))
                top_one_logit = np.take_along_axis(top_k_logits, top_one_logit_local_idx, axis=1)
                top_one_logit_idx = np.take_along_axis(top_k_logit_idxs, top_one_logit_local_idx, axis=1)
                labels = np.array(line['labels'])

                # currently only support single example per line 
                top_logits = top_one_logit.reshape(-1)
                top_logit_idxs = top_one_logit_idx.reshape(-1)

                is_correct = top_logit_idxs == labels

                for timestep in range(top_logits.shape[0]):
                    if labels[timestep] == 0:
                        # hit EOS, break
                        break
                    all_top_preds.append(top_logits[timestep])
                    all_is_correct.append(is_correct[timestep])

        return (np.array(all_top_preds), np.array(all_is_correct))

