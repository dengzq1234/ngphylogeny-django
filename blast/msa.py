
class PseudoMSA:
    """
    This class represents a pseudo Multiple Sequence alignment
    That will be build from a BLAST result and having the following
    properties:
    - columns having GAPS in the query are removed
    - subjects having several hsps are merged in the
    same sequence, filled with gaps around
    """

    query_id = ""
    query_seq = ""
    sequences = dict()  # Dict: key: seqname, value: sequence

    def __init__(self, query_id, query_seq):
        """
        query : blast query sequence without gaps
        """
        self.query_id = str(query_id)
        self.query_seq = list(query_seq)

    def add_hsp(self, sbjct_name, hsp):
        """
        sbjct_name: name of the subject sequence
        hsp: Bio.Blast.Record.HSP
        """
        seq = self.sequences.get(str(sbjct_name))
        if seq is None:
            seq = list("-" * len(self.query_seq))
        start = hsp.query_start
        position = start-1
        for p in range(0, len(hsp.sbjct)):
            # If no gap in the query at that position
            if hsp.query[p] != '-':
                if hsp.sbjct[p] != '-':
                    seq[position] = hsp.sbjct[p]
                position += 1
        self.sequences[str(sbjct_name)] = seq

    def all_sequences(self):
        for id, seq in self.sequences.iteritems():
            yield (str(id), "".join(seq))

    def to_string(self):
        msa = ">%s\n%s\n" % (self.query_id, "".join(self.query_seq))
        for id, seq in self.sequences.iteritems():
            msa += ">%s\n%s\n" % (id, "".join(seq))
        return msa