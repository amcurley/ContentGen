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
caching.clear_cache()

arg = """
Title: EMBARRASSING STORIES FROM MY TRAVELS
Body: I visited Argentina for the first time the year before I started working as a lawyer in New York City. Up until that point, my Spanish vocabulary consisted of very basic words I learned and strung together while visiting Spain. It was in Barcelona, in between tapas and wine, that I learned some phrases that kept me afloat in more rural areas.

Where is the bathroom?

How are you?

I am from Canada.

My name is Jodi.

Where can I take the bus?

It was the latter sentence that got me into trouble in Argentina. Coming off a long bus ride, I couldn’t find my connecting bus. I approached two men wearing the Andesmar uniform, thinking they might know.

“Permiso donde puedo coger el bus?” I asked timidly. I thought what I was asking was, “where can I take the bus?”

I was met with raucous laughter.

“Donde quieres, chica!” one of them said.

Confusion reigned until I remembered what my friends in Uruguay told me: coger was slang for “to fuck.”

So I basically asked where could fuck the bus, which led to the mirthful, mocking response of “wherever you’d like, lady.”

Face flushed with shame, I blurted out, “lo siento, estoy tanto embarazada!”

The gentlemen doubled over with laughter once again. One looked me up and down slowly and drawled, “I think not” (“pienso que no”).

And that was how I learned that in Spanish, embarazada is the word for “pregnant,” not for embarrassed. In case you were wondering, embarrassed is avergonzado or desconcertado.

For those learning Spanish, there are several other words that resemble English words but aren’t. A few:

Librería is a book store, not a library. A library is a biblioteca.
Decepción means to be disappointed, not deceived. A deception is an engaño.
And one of my favourites: carpeta is a file folder — a carpet is the awesome alfombra. Carpet never sounded so satisfying.
As for Argentina, I was appalled to manage not one but two disastrous language mistakes. To assuage my shame, I wrote a group email back to friends and family at home.

Title: AN ACONGACUA CLIMB IN ARGENTINA
Body: I spent 3 and a half weeks in Argentina — a few days in Mendoza, 2 weeks on an expedition to climb Aconcagua (6,962 meters (22,841 feet)), a few days at Iguazu Falls and a few days in Buenos Aires. I’m not sure what would compel someone who grew up in humid, hot and flat Texas to want to climb mountains. For most there would be little allure in altitude headaches, nausea, opportunities for frostbite and edema, lack of opportunities to take a shower or an unobserved toilet break, et cetera. Say what one will, I love climbing because I’m fascinated by soaring, rugged peaks and the knowledge and experience required to ascend and survive them. Mountains were the reason I moved from Manhattan to Colorado 2 years ago, and on December 27, 2008, instead of flying to a beach as one might expect, I flew to Mendoza to experience Argentina’s snowy white peaks. I spent a few days in New York around Christmas, hanging out with family and friends, before heading to Argentina and lucky for me, Jodi (I miss you!) was there for a couple days and we were able to catch up over sushi, cornbread and soup at Whole Foods in Columbus Circle.

On the Miami-Santiago leg of my flight, I ran into Elaine, a woman who lived on the same hall as me freshman year when we were undergrads. Coincidentally, she, her husband and 2 adorable children were also on their way to Mendoza and totally randomly, she and I stayed in adjacent rooms for a night in Mendoza. We landed in Mendoza a couple hours later than expected because our flight out of Santiago was turned back about 15 minutes into the flight. We could smell fumes in the cabin and we weren’t flying very high off the ground, even though we were supposed to be flying over the Andes mountains, past el cumbre de Aconcagua. Mendoza was warm and breezy with clean, tree-lined streets. Anecdotes about how attractive Argentinians are proved to be true — after a few days of eating asado, pizza, matambre sandwiches and helado, though, I wondered how the women stayed so petite. The next day, our guides checked our equipment and we met the other members of our expedition group over dinner — there were 12 in all (8 men, 4 women) — 5 Australians, 1 Swiss, 2 Canadians, 1 Argentinian, 1 Pole, 1 Irish and 1 American (me).

Title: EL CALAFATE AND PERITO MORENO GLACIER
Body: Glancing through the pictures of the glacier will not even remotely express what it feels like to stand in front of it. Because of a small break in the towering Andes, water from storms on the west coast carries eastward and blankets the 48 glaciers in Chilean and Argentine Patagonia with snow. The Perito Moreno glacier is one of the few that is considered ‘stable’, meaning that it is not retreating (other glaciers in the same national park are in retreat) and it marches forward over Lago Argentino, hitting the peninsula in the middle of the lake. At this point, the water in the Brazo Rico (rich arm) of Lago Argentino is over 30m higher than on the other side of the peninsula – ’tis a lot of pressure of frozen water basically smushing itself into the land. The resulting tension causes sporadic ruptures in the glacier. The last big rupture was in 2006, and i can only imagine the auditory and visual spectacle that it must have wrought. i stood on the ramparts watching the glacier for hours and the small chunks that tumbled into the lake made such a clamouring, thunderous noise that a rupture must be unbelievable.

Perito Moreno is not, as I initially thought, a ‘small dog moreno’ (incidentally, small dog is perrito not perito, as i learnt). Perito means specialist and Francisco Moreno, explorer and knower of all things border related was appointed perito in the early 1900s for his knowledge about border conflicts (and ostensibly his strident defense of Argentina in its attempts to defend its borders against Chile).

"""


def interact_model(input_text,
    model_name='124M',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=40,
    temperature=0.7,
    top_k=0,
    top_p=1,
    models_dir='gpt/models',
    # input_text
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
                hparams=hparams, length=length,
                context=context,
                batch_size=batch_size,
                temperature=temperature, top_k=top_k, top_p=top_p
            )

            saver = tf.train.Saver()
            ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
            saver.restore(sess, ckpt)

            while True:
                raw_text = input_text
                while not raw_text:
                    print('Prompt should not be empty!')
                    st.markdown('Prompt should not be empty!')
                    raw_text = arg + "Title: " + input_text + "Body: "
                context_tokens = enc.encode(raw_text)
                generated = 0
                for _ in range(nsamples // batch_size):
                    out = sess.run(output, feed_dict={
                        context: [context_tokens for _ in range(batch_size)]
                    })[:, len(context_tokens):]
                    for i in range(batch_size):
                        generated += 1
                        text = enc.decode(out[i])
                        st.markdown(text)
                        st.stop()

# User text input function
def text_input(text):
    return text

def write():
    """Method used to bring page into the app.py file"""
    with st.spinner("Loading ..."):
        st.title("Generate Your Blog Post!")
        st.markdown(
        """
        **Tutorial:**

        - Enter the title of your blog post below.
        - Click enter/return
        - Click "Generated Your Blog Post" (this may take around 20 seconds to generate)
        - Boom! You now have a body for your blog post.

        **Caution:** This model was trained on data from the internet
        so there might be bias and facutal inaccuracies. If you are not happy with the result generated just click the button again!

        These blogs will not be perfect but they serve as a solid starting ground for anyone who is having trouble with writers block.

        Enjoy "writing"

        """)
        hmm = text_input(st.text_input("Enter Title Here"))
        texter = interact_model(hmm, model_name='124M',
        seed=None,
        nsamples=1,
        batch_size=1,
        length=300,
        temperature=0.7,
        top_k=0,
        top_p=1,
        models_dir='gpt/models',
        # hmm
        )
