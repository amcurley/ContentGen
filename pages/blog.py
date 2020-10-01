import streamlit as st
import awesome_streamlit as ast
import fire
import json
import os
import numpy as np
import tensorflow as tf
import gpt.src.model as model
import gpt.src.sample as sample
import gpt.src.encoder as encoder
import time
import sys
from streamlit import caching
import numpy as np
caching.clear_cache()

def interact_model(box_selection, input_text,
    model_name='124M',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=40,
    temperature=0.7,
    top_k=0,
    top_p=1,
    models_dir='gpt/models',
):
    if st.button('Run GPT-2'):
        st.markdown("Body Text:")
        models_dir = os.path.expanduser(os.path.expandvars(models_dir))
        if batch_size is None:
            batch_size = 1
        assert nsamples % batch_size == 0

        enc = encoder.get_encoder(model_name, models_dir)
        hparams = model.default_hparams()
        with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))

        if length is None:
            length = hparams.n_ctx // 2
        elif length > hparams.n_ctx:
            raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

        with tf.Session(graph=tf.Graph()) as sess:
            context = tf.placeholder(tf.int32, [batch_size, None])
            np.random.seed(seed)
            tf.set_random_seed(seed)
            # Tokens created from the sample
            output = sample.sample_sequence(
                hparams=hparams,
                length=length,
                # length=1023,
                context=context,
                batch_size=batch_size,
                temperature=temperature, top_k=top_k, top_p=top_p
            )

            saver = tf.train.Saver()
            ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
            saver.restore(sess, ckpt)

            while True:
                raw_text = box_selection + input_text
                # print(raw_text)
                while not raw_text:
                    print('Prompt should not be empty!')
                    st.markdown('Prompt should not be empty!')
                    raw_text = box_selection + "Title: " + input_text + " Body: "
                    # print(raw_text)
                context_tokens = enc.encode(raw_text)
                generated = 0
                for _ in range(nsamples // batch_size):
                    out = sess.run(output, feed_dict={
                        context: [context_tokens for _ in range(batch_size)]
                    })[:, len(context_tokens):]
                    for i in range(batch_size):
                        generated += 1
                        text = enc.decode(out[i])
                        text = text + "."
                        st.markdown(text)
                        st.success("Nice Blog!")
                        st.stop()

# User text input function
def text_input(text):
    if text == '':
        text = ' '
    return text

def boxes():
    option = st.selectbox('Select one example topic below!',
    ('Choose a Topic', 'Argentina', 'Random'))

    if option == 'Choose a Topic':
        message = ""
    elif option == 'Argentina':
        f = open('./pages/argentina.txt', "r" ) # I will need a few .txt files
        message = f.read()
    else:
        message = ""

    return message


def write():
    """Method used to bring page into the app.py file"""
    with st.spinner("Loading ..."):
        st.title("Generate Your Blog Post!")
        st.markdown(
        """
        **Tutorial:**

        1. Choose one of the selected topics. If you do not see a topic that you are interested in just move onto step 2.
        2.  Enter the title of your blog post below.
        3. Click enter/return
        4. Click "Generated Your Blog Post" (this may take around 20 seconds to generate)
        5. Boom! You now have a body for your blog post.

        **Caution:** This model was trained on data from the internet
        so there might be bias and facutal inaccuracies. If you are not happy with the result generated just click the button again!

        These blogs will not be perfect but they serve as a solid starting ground for anyone who is having trouble with writers block.

        Enjoy "writing"

        """)
        box_selection = boxes()
        hmm = text_input(st.text_input("Enter Title Here"))
        texter = interact_model(box_selection, hmm, model_name='124M',
        seed=None,
        nsamples=3,
        batch_size=1,
        length=300,
        temperature=0.7,
        top_k=0,
        top_p=1,
        models_dir='gpt/models',
        # hmm
        )
