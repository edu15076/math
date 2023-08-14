/**
 * This function elevates <b>e</b> to the <b>x</b> with extreme precision. It's good to alert that a normal <b>pow()</b>
 * function may be faster but less precise.<br>
 *
 * This method is defined in Continued Fractions, Vol. 1: Convergence Theory. From: Lisa Lorentzen and Haakon Waadeland.
 * @param x the number to elevate <b>e</b>.
 * @return <b>e</b> to the power of <b>x</b>.
 */
double exp_c(double x) {
    double xsqr = x * x;
    int n = (10 + (int) x) * 4 - 2;
    __float128 sum = n + 4;
    for ( ; n != 2; n -= 4)
        sum = n + xsqr / sum;

    return 1 + 2 * x / (2 - x + xsqr / sum);
}
