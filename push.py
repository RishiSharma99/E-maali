from pywebpush import webpush

def push(subi):
	webpush(
		subi,
		"",
		vapid_private_key="WsRleynSjjH2AbE4d9EYxkyP_VhIE3kVrLjgx2XN7Ic",
        vapid_claims={"sub": "mailto:rishi17260@iiitd.ac.in"}
	)