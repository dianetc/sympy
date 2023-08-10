from hypothesis import given, assume
from hypothesis import strategies as st
from sympy.abc import x
from sympy.polys.polytools import Poly


@st.composite
def coeffecients(draw: st.DrawFn):
    l = draw(st.lists(st.integers()))
    if len(l) > 0:
        assume(l[0] != 0)
    return l


@given(
    coefficients1=coeffecients(),
    coefficients2=coeffecients(),
    coefficients3=coeffecients(),
)
def test_gcd(coefficients1, coefficients2, coefficients3):
    f = Poly(coefficients1, x, domain="ZZ")
    g = Poly(coefficients2, x, domain="ZZ")
    r = Poly(coefficients3, x, domain="ZZ")

    gcd_1 = f.gcd(g)
    gcd_2 = g.gcd(f)

    assert gcd_1 == gcd_2

    # multiply by r
    gcd_3 = g.gcd(f + r * g)

    assert gcd_1 == gcd_3


@given(
    coefficients1=coeffecients(),
    coefficients2=st.lists(st.integers().filter(lambda n: n != 0), min_size=1),
)
def test_division(coefficients1, coefficients2):
    # Integer case
    f_z = Poly(coefficients1, x, domain="ZZ")
    g_z = Poly(coefficients2, x, domain="ZZ")
    remainder_z = f_z.rem(g_z)
    assert g_z.degree() >= remainder_z.degree() or remainder_z.degree() == 0

    # Rational case
    f_q = Poly(coefficients1, x, domain="QQ")
    g_q = Poly(coefficients2, x, domain="QQ")
    remainder_q = f_q.rem(g_q)
    assert g_q.degree() >= remainder_q.degree() or remainder_q.degree() == 0


@given(
    coefficients1=coeffecients(),
    coefficients2=coeffecients(),
)
def test_multiplication(coefficients1, coefficients2):
    f = Poly(coefficients1, x, domain="ZZ")
    g = Poly(coefficients2, x, domain="ZZ")
    h = f * g
    assert h.degree() == f.degree() + g.degree()
    assert h.LC() == f.LC() * g.LC()


@given(
    coefficients1=coeffecients(),
    coefficients2=coeffecients(),
)
def test_addition(coefficients1, coefficients2):
    f = Poly(coefficients1, x, domain="ZZ")
    g = Poly(coefficients2, x, domain="ZZ")
    h = f + g
    assert h.degree() == max(f.degree(), g.degree())


@given(
    coefficients1=coeffecients(),
    coefficients2=st.lists(st.integers().filter(lambda n: n != 0), min_size=1),
)
def test_lcm(coefficients1, coefficients2):
    f = Poly(coefficients1, x, domain="ZZ")
    g = Poly(coefficients2, x, domain="ZZ")
    assert f.lcm(g) == (f * g).quo(f.gcd(g))


@given(
    coefficients=coeffecients(),
    value=st.integers(),
)
def test_dispersion(coefficients, value):
    f = Poly(coefficients, x, domain="ZZ")
    g = Poly([value], x, domain="ZZ")
    assert f.dispersion() == f.dispersion(f)
    assert f.dispersion(g) == 0
