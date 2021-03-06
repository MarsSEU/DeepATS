import argparse
import logging
import os

def parse_args(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out-dir", dest="out_dir_path", type=str, metavar='<str>', required=True, help="The path to the output directory")
    parser.add_argument("-p", "--prompt", dest="prompt_id", type=int, metavar='<int>', required=False, help="Promp ID for ASAP dataset. '0' means all prompts.")
    parser.add_argument("-t", "--type", dest="model_type", type=str, metavar='<str>', default='regp', help="Model type (reg|regp|breg|bregp) (default=regp)")
    parser.add_argument("-u", "--rec-unit", dest="recurrent_unit", type=str, metavar='<str>', default='lstm', help="Recurrent unit type (lstm|gru|simple) (default=lstm)")
    parser.add_argument("-a", "--algorithm", dest="algorithm", type=str, metavar='<str>', default='rmsprop', help="Optimization algorithm (rmsprop|sgd|adagrad|adadelta|adam|adamax) (default=rmsprop)")
    parser.add_argument("-l", "--loss", dest="loss", type=str, metavar='<str>', default='mse', help="Loss function (mse|mae) (default=mse)")
    parser.add_argument("-e", "--embdim", dest="emb_dim", type=int, metavar='<int>', default=50, help="Embeddings dimension (default=50)")
    parser.add_argument("-c", "--cnndim", dest="cnn_dim", type=int, metavar='<int>', default=0, help="CNN output dimension. '0' means no CNN layer (default=0)")
    parser.add_argument("-w", "--cnnwin", dest="cnn_window_size", type=int, metavar='<int>', default=3, help="CNN window size. (default=3)")
    parser.add_argument("-r", "--rnndim", dest="rnn_dim", type=int, metavar='<int>', default=300, help="RNN dimension. '0' means no RNN layer (default=300)")
    parser.add_argument("-b", "--batch-size", dest="batch_size", type=int, metavar='<int>', default=32, help="Batch size (default=32)")
    parser.add_argument("-v", "--vocab-size", dest="vocab_size", type=int, metavar='<int>', default=4000, help="Vocab size (default=4000)")
    parser.add_argument("--aggregation", dest="aggregation", type=str, metavar='<str>', default='mot', help="The aggregation method for regp and bregp types (mot|attsum|attmean) (default=mot)")
    parser.add_argument("--dropout", dest="dropout_prob", type=float, metavar='<float>', default=0.5, help="The dropout probability. To disable, give a negative number (default=0.5)")
    parser.add_argument("--vocab-path", dest="vocab_path", type=str, metavar='<str>', help="(Optional) The path to the existing vocab file (*.pkl)")
    parser.add_argument("--skip-init-bias", dest="skip_init_bias", action='store_true', help="Skip initialization of the last layer bias")
    parser.add_argument("--emb", dest="emb_path", type=str, metavar='<str>', help="The path to the word embeddings file (Word2Vec format)")
    parser.add_argument("--epochs", dest="epochs", type=int, metavar='<int>', default=100, help="Number of epochs (default=50)")
    parser.add_argument("--maxlen", dest="maxlen", type=int, metavar='<int>', default=0, help="Maximum allowed number of words during training. '0' means no limit (default=0)")
    parser.add_argument("--seed", dest="seed", type=int, metavar='<int>', default=1234, help="Random seed (default=1234)")
    ## dsv
    parser.add_argument("--min-word-freq", dest="min_word_freq", type=int, metavar='<int>', default=2, help="Min word frequency")
    parser.add_argument("--stack", dest="stack", type=int, metavar='<int>', default=1, help="how deep to stack core RNN")
    parser.add_argument("--skip-emb-preload", dest="skip_emb_preload", action='store_true', help="Skip preloading embeddings")
    parser.add_argument("--tokenize-old", dest="tokenize_old", action='store_true', help="use old tokenizer")
    
    parser.add_argument("-ar", "--abs-root", dest="abs_root", type=str, metavar='<str>', required=False, help="Abs path to root directory")
    parser.add_argument("-ad", "--abs-data", dest="abs_data", type=str, metavar='<str>', required=False, help="Abs path to data directory")
    parser.add_argument("-ao", "--abs-out", dest="abs_out", type=str, metavar='<str>', required=False, help="Abs path to output directory")
    parser.add_argument("-dp", "--data-path", dest="data_path", type=str, metavar='<str>', required=False, help="Abs path to output directory")
    ##
    
    if argv is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(argv)
        
    return args

def get_args():
    
    prompt = '61891'
    # 57452 54147 61693 61915 70086* 61875 
    # 55433 61247 61352* 54735 61923* 55417* 55403
    # 55052 62037 61891
    #################
    
    dataroot = '/home/david/data/ats/ets'
    datapath = os.path.join(dataroot, prompt)
    
    deepatsroot = '/home/david/code/python/DeepATS'
    outroot = os.path.join(deepatsroot, 'output')
    
    args = '-o output'
    argv = args.split()
    
    argv.append('--prompt'); argv.append(prompt)
    
    argv.append('--batch-size'); argv.append('32')
    #argv.append('--batch-size'); argv.append('64')
    #argv.append('--batch-size'); argv.append('128')
    
    
    argv.append('--loss'); argv.append('kappa')
    #argv.append('--loss'); argv.append('soft_kappa')
    #argv.append('--loss'); argv.append('mse')
    
    #argv.append('--emb'); argv.append('/home/david/data/embed/glove.6B.50d.txt')
    #argv.append('--emb'); argv.append('/home/david/data/embed/glove.6B.100d.txt'); argv.append('--embdim'); argv.append('100');
    #argv.append('--emb'); argv.append('/home/david/data/embed/glove.6B.200d.txt'); argv.append('--embdim'); argv.append('200');
    argv.append('--emb'); argv.append('/home/david/data/embed/glove.6B.{}d.txt'); argv.append('--embdim'); argv.append('300');
    
    #argv.append('--emb'); argv.append('/home/david/data/embed/lexvec.commoncrawl.300d.W.pos.neg3.txt'); argv.append('--embdim'); argv.append('300');
    
    #argv.append('--emb'); argv.append('/home/david/data/embed/fasttext.sg.100d.txt'); argv.append('--embdim'); argv.append('100');##BEST
    #argv.append('--emb'); argv.append('/home/david/data/embed/fasttext.sg.200d.m1.txt'); argv.append('--embdim'); argv.append('200');
    #argv.append('--emb'); argv.append('/home/david/data/embed/fasttext.sg.200d.m2.txt'); argv.append('--embdim'); argv.append('200');
    #argv.append('--emb'); argv.append('/home/david/data/embed/fasttext.cb.200d.m2.txt'); argv.append('--embdim'); argv.append('200');
    #argv.append('--emb'); argv.append('/home/david/data/embed/fasttext.6033.200d.txt'); argv.append('--embdim'); argv.append('200');
    
    #argv.append('--emb'); argv.append('/home/david/data/embed/sswe.w5.100d.txt'); argv.append('--embdim'); argv.append('100');
    
    #argv.append('--vocab-size'); argv.append('2560')
    
    argv.append('--rec-unit'); argv.append('rwa')
    #argv.append('--stack'); argv.append('2')
    
    #argv.append('--cnndim'); argv.append('64')
    #argv.append('--rnndim'); argv.append('167')
    #argv.append('--rnndim'); argv.append('200')
    #argv.append('--rnndim'); argv.append('250')
    argv.append('--rnndim'); argv.append('300')
        
    #argv.append('--dropout'); argv.append('0.46')
    argv.append('--dropout'); argv.append('0.5')

    #argv.append('--aggregation'); argv.append('attsum')
    #argv.append('--aggregation'); argv.append('attmean')
    
    #argv.append('--type'); argv.append('bregp'); argv.append('--skip-init-bias')
    
    #argv.append('--algorithm'); argv.append('sgd')
    #argv.append('--algorithm'); argv.append('adagrad')
    
    #argv.append('--seed'); argv.append('0')
    argv.append('--seed'); argv.append('4357638')
    
    #argv.append('--skip-emb-preload')
    #argv.append('--tokenize-old')
    argv.append('--min-word-freq'); argv.append('2')
    
    argv.append('--abs-root'); argv.append(deepatsroot)
    argv.append('--abs-data'); argv.append(dataroot)
    argv.append('--abs-out'); argv.append(outroot)
    argv.append('--data-path'); argv.append(datapath)
    
    argv.append('--epochs'); argv.append('30')
    
    return parse_args(argv)
