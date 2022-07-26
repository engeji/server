from flask import Flask, render_template, request, jsonify, make_response, request
from spch_module.comp2 import Comp2
from spch_module.mode2 import Mode2

app = Flask(__name__)

@app.route('/')
def index():
    comp_obj = Comp2(type_spch=['ГПА-ц3-16С-45-1.7(ККМ)', 'ГПА Ц3 16с76-1.7М'], w_cnt=[1,2])
    res = comp_obj.calc_via_p_in(Mode2(), [5200]*2)
    return repr(res)

if __name__ == '__main__':
    app.run()