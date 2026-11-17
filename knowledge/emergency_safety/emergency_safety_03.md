# 应急与安全 · 第8册_逻辑统计数学工具箱技术编程实战

        self._prev = set(_prev)
        self._op = _op
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out
    def __pow__(self, other):
        assert isinstance(other, (int, float))
        out = Value(self.data ** other, (self,), f'**{other}')
        def _backward():
            self.grad += other * (self.data ** (other - 1)) * out.grad
        out._backward = _backward
        return out
    def relu(self):
        out = Value(0 if self.data < 0 else self.data, (self,), 'ReLU')
        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        return out
    def backward(self):
        topo, visited = [], set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad = 1.0
        for v in reversed(topo):
            v._backward()
# ========== 3. Transformer Block (simplified) ==========
class Neuron:
    def __init__(self, nin):
        self.w = [Value(random.uniform(-1, 1)) for _ in range(nin)]
        self.b = Value(random.uniform(-1, 1))
    def __call__(self, x):
        act = self.b
        for wi, xi in zip(self.w, x):
            act = act + wi * xi
        return act.relu()
class Layer:
    def __init__(self, nin, nout):
        self.neurons = [Neuron(nin) for _ in range(nout)]
    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out) == 1 else out
# ========== 4. GPT-style Model ==========
class GPT:
    def __init__(self, vocab_size, block_size, n_embd=64, n_head=4):
        self.vocab_size = vocab_size
        self.block_size = block_size
        self.n_embd = n_embd
        self.token_emb = [[random.uniform(-0.1, 0.1) for _ in range(n_embd)]
                          for _ in range(vocab_size)]
        self.pos_emb = [[random.uniform(-0.1, 0.1) for _ in range(n_embd)]
                        for _ in range(block_size)]
        self.head = Layer(n_embd, vocab_size)
    def forward(self, idx):
        B = len(idx)
        T = min(len(idx[0]), self.block_size)
        logits = []
        for b in range(B):
            row = []
            for t in range(T):
                tok = self.token_emb[idx[b][t]]
                pos = self.pos_emb[t]
                hidden = [tok[i] + pos[i] for i in range(self.n_embd)]
                logit = self.head(hidden)
                row.append(logit)
            logits.append(row)
        return logits
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            idx_cond = [row[-self.block_size:] for row in idx]
            logits = self.forward(idx_cond)
            # take the last position's logits
            last = logits[0][-1]
            # argmax (greedy)
            next_idx = max(range(len(last)), key=lambda i: last[i].data)
            idx[0].append(next_idx)
        return idx