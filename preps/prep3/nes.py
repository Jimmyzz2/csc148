class  F:
    pass
class H(F):
    pass

class G(F):
    pass

class V(G):
    pass

if __name__ == "__main__":
    f = F()
    g = G()
    h = H()
    v = V()
    print(isinstance(h, F) == True)
    print(isinstance(g, H) == False)
    print((type(f) == type (g)) == False)
    print((type(g) == type(h)) == False)
    print(isinstance(g, F) == True)
    print(isinstance(h, G) == False)
    print(isinstance(v, F) == True)