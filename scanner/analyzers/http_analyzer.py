from scanner.models.finding import Finding


class HTTPAnalyzer:
    """
    Performs security analysis on HTTP enumeration data.
    """

    SECURITY_HEADERS = {
        "Strict-Transport-Security": (
            "Medium",
            "Missing HSTS Header",
            "HTTP Strict Transport Security (HSTS) is not configured.",
            "Enable the Strict-Transport-Security header."
        ),

        "Content-Security-Policy": (
            "Medium",
            "Missing Content Security Policy",
            "No Content Security Policy (CSP) header was found.",
            "Configure the Content-Security-Policy header."
        ),

        "X-Frame-Options": (
            "Medium",
            "Missing X-Frame-Options",
            "The application can potentially be embedded in iframes.",
            "Set X-Frame-Options to DENY or SAMEORIGIN."
        ),

        "X-Content-Type-Options": (
            "Low",
            "Missing X-Content-Type-Options",
            "Browsers may MIME-sniff responses.",
            "Set X-Content-Type-Options to 'nosniff'."
        ),

        "Referrer-Policy": (
            "Low",
            "Missing Referrer Policy",
            "The browser may leak referrer information.",
            "Configure an appropriate Referrer-Policy."
        )
    }

    def analyze(self, http: dict) -> list[Finding]:

        findings = []

        findings.extend(
            self.check_security_headers(http)
        )

        findings.extend(
            self.check_server_disclosure(http)
        )

        findings.extend(
            self.check_powered_by(http)
        )

        return findings

    # --------------------------------------------------------

    def check_security_headers(self, http: dict) -> list[Finding]:

        findings = []

        headers = http.get(
            "security_headers",
            {}
        )

        for header, details in self.SECURITY_HEADERS.items():

            if headers.get(header) == "Missing":

                severity, title, description, recommendation = details

                findings.append(

                    Finding(

                        severity=severity,

                        title=title,

                        description=description,

                        recommendation=recommendation

                    )

                )

        return findings

    # --------------------------------------------------------

    def check_server_disclosure(self, http: dict) -> list[Finding]:

        findings = []

        server = http.get(
            "server",
            ""
        )

        if "/" in server:

            findings.append(

                Finding(

                    severity="Low",

                    title="Server Version Disclosure",

                    description=(
                        f"The server header exposes "
                        f"'{server}'."
                    ),

                    recommendation=(
                        "Hide or minimize version "
                        "information in the Server header."
                    )

                )

            )

        return findings

    # --------------------------------------------------------

    def check_powered_by(self, http: dict) -> list[Finding]:

        findings = []

        powered_by = http.get(
            "powered_by",
            ""
        )

        if powered_by:

            findings.append(

                Finding(

                    severity="Low",

                    title="Technology Disclosure",

                    description=(
                        f"X-Powered-By exposes "
                        f"'{powered_by}'."
                    ),

                    recommendation=(
                        "Remove or suppress the "
                        "X-Powered-By header."
                    )

                )

            )

        return findings