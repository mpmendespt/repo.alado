import base64, codecs
magic = 'aW1wb3J0IG9zLCB4Ym1jLCB4Ym1jYWRkb24KCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwojIyMgVXNlciBFZGl0IFZhcmlhYmxlcyAjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCkFERE9OX0lEICAgICAgID0geGJtY2FkZG9uLkFkZG9uKCkuZ2V0QWRkb25JbmZvKCdpZCcpCkFERE9OVElUTEUgICAgID0gJ01pbGhhbm8gVGhlbWVzJwpFWENMVURFUyAgICAgICA9IFtBRERPTl9JRF0KIyBUZXh0IEZpbGUgd2l0aCBidWlsZCBpbmZvIGluIGl0LgpCVUlMREZJTEUgICAgICA9ICdodHRwczovL21pbGhhbm8uY29tLnB0L3dpemFyZC90ZW1hLnR4dCcKIyBIb3cgb2Z0ZW4geW91IHdvdWxkIGxpc3QgaXQgdG8gY2hlY2sgZm9yIGJ1aWxkIHVwZGF0ZXMgaW4gZGF5cwojIDAgYmVpbmcgZXZlcnkgc3RhcnR1cCBvZiBrb2RpClVQREFURUNIRUNLICAgID0gMAojIFRleHQgRmlsZSB3aXRoIGFwayBpbmZvIGluIGl0LgpBUEtGSUxFICAgICAgICA9ICdodHRwOi8vJwojIFRleHQgRmlsZSB3aXRoIFlvdXR1YmUgVmlkZW9zIHVybHMuICBMZWF2ZSBhcyAnaHR0cDovLycgdG8gaWdub3JlCllPVVRVQkVUSVRMRSAgID0gJycKWU9VVFVCRUZJTEUgICAgPSAnaHR0cDovLycKIyBUZXh0IEZpbGUgZm9yIGFkZG9uIGluc3RhbGxlci4gIExlYXZlIGFzICdodHRwOi8vJyB0byBpZ25vcmUKQURET05GSUxFICAgICAgPSAnaHR0cDovLycKIyBUZXh0IEZpbGUgZm9yIGFkdmFuY2VkIHNldHRpbmdzLiAgTGVhdmUgYXMgJ2h0dHA6Ly8nIHRvIGlnbm9yZQpBRFZBTkNFREZJTEUgICA9ICdodHRwOi8vJwoKIyBEb250IG5lZWQgdG8gZWRpdCBqdXN0IGhlcmUgZm9yIGljb25zIHN0b3JlZCBsb2NhbGx5ClBBVEggICAgICAgICAgID0geGJtY2FkZG9uLkFkZG9uKCkuZ2V0QWRkb25JbmZvKCdwYXRoJykKQVJUICAgICAgICAgICAgPSBvcy5wYXRoLmpvaW4oUEFUSCwgJ3Jlc291cmNlcycsICdhcnQnKQoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCiMjIyBUSEVNSU5HIE1FTlUgSVRFTVMgIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjI'
love = 'lZwVlZXVlOWMvO5o3Htq2ShqPO0olO1p2HtoT9wLJkfrFOmqT9lMJDtnJAioaZtqTuyVUOfLJAyVUEbMJ0tnJ4tqTuyVSWyp291pzAypl9OpaDiPvZtMz9fMTIlVT9zVUEbMFO3nKcupzDtqTuyovO1p2Hto3ZhpTS0nP5do2yhXRSFIPjtW2ygLJqyozSgMF5jozpaXDbwVTEiVT5iqPOjoTSwMFOkqJ90MKZtLKWiqJ5xVT9mYaOuqTthnz9cotbwVRI4LJ1joTH6VPOWD09BGHSWGyDtVPNtVQ0to3ZhpTS0nP5do2yhXRSFIPjtW21unJ50nJAiov5jozpaXDbwVPNtVPNtVPNtVPOWD09BH0IHIRyBE1ZtVQ0tW2u0qUOmBv8inF5coJq1pv5wo20iDJVmZTM4Fl5jozpaPvZtGTIuqzHtLKZtnUE0pQbiYlOzo3VtMTIzLKIfqPOcL29hPxyQG05PIHyZESZtVPNtVQ0tW2u0qUOmBv8inF5coJq1pv5wo20iIUOfL0uIEP5jozpaPxyQG05ADHyBIPNtVPNtVQ0tW2u0qUOmBv8inF5coJq1pv5wo20inUA6nxZ0ql5jozpaPxyQG05OHRftVPNtVPNtVQ0tW2u0qUOmBv8iWjcWD09BDHERG05GVPNtVPN9VPqbqUEjBv8iWjcWD09BJH9IISIPEFNtVPN9VPqbqUEjpmbiYlpXFHACGyAOIxHtVPNtVPNtCFNanUE0pUZ6Yl9cYzygM3IlYzAioF9Xo3DjH1WFYaOhMlpXFHACGyEFDHgHVPNtVPNtCFNanUE0pQbiYlpXFHACGyWSDHjtVPNtVPNtCFNanUE0pQbiYlpXFHACGxkCE0yBVPNtVPNtCFNanUE0pQbiYlpXFHACGxACGyEOD1DtVPNtCFNanUE0pUZ6Yl9cYzygM3IlYzAioF9mqRSAG25BYaOhMlpXFHACGyASISEWGxqGVPNtCFNanUE0pUZ6Yl9cYzygM3IlYzAioF9OLwZjMauYYaOhMlpXVlOVnJEyVUEbMFN9CG09CG0tp2IjMKWuqT9lplNaJJImWlOipvNaGz8aPxuWERIGHRSQEIWGVPNtVQ0tW05iWjbwVRAbLKWuL3EypvO1p2IxVTyhVUAypTIlLKEiptcGHRSQEIVtVPNtVPNtVPN9VPpdXvpXPvZtJJ91VTAuovOyMTy0VUEbMKAyVTuiq2I2MKVtrJ91VUquoaDfVTc1p3DtoJSeMFOmqKWyVUEbLKDtrJ91VTuuqzHtLFNyplOcovOyLJAbVT9zVUEbMDbwVSEVEH1SW3Ztp28tnKDtM3WuLaZtqTuyVUEyrUDtMaWioFO0nTHtoJIhqFOcqTIgPxACGR9FZFNtVPNtVPNtVQ0tW3qbnKEyWjcQG0kCHwVtVPNtVPNtVPN9VPqipzShM2HaPvZtHUWcoJSlrFOgMJ51VTy0MJ1mVPNtYlNyplOcplO0nTHtoJIhqFOcqTIgVTShMPOcplOlMKS1nKWyMNcHFRIAEGRtVPNtVPNtVPN9VPqoD09ZG1VtWlgQG0kCHwReW11oDy1oFI0bJ0ACGR9FVPpeD09ZG1VlXlqqGJyfnTSho1fiD09ZG1WqXIfiDy'
god = '1bL0NPTE9SXSBbQ09MT1IgJytDT0xPUjIrJ10lc1svQ09MT1JdWy9JXScKIyBCdWlsZCBOYW1lcyAgICAgICAgICAvICVzIGlzIHRoZSBtZW51IGl0ZW0gYW5kIGlzIHJlcXVpcmVkClRIRU1FMiAgICAgICAgID0gJ1tDT0xPUiAnK0NPTE9SMisnXSVzWy9DT0xPUl0nCiMgQWx0ZXJuYXRlIGl0ZW1zICAgICAgLyAlcyBpcyB0aGUgbWVudSBpdGVtIGFuZCBpcyByZXF1aXJlZApUSEVNRTMgICAgICAgICA9ICdbQ09MT1IgJytDT0xPUjErJ10lc1svQ09MT1JdJwojIEN1cnJlbnQgQnVpbGQgSGVhZGVyIC8gJXMgaXMgdGhlIG1lbnUgaXRlbSBhbmQgaXMgcmVxdWlyZWQKVEhFTUU0ICAgICAgICAgPSAnW0NPTE9SICcrQ09MT1IxKyddQ3VycmVudCBCdWlsZDpbL0NPTE9SXSBbQ09MT1IgJytDT0xPUjIrJ10lc1svQ09MT1JdJwojIEN1cnJlbnQgVGhlbWUgSGVhZGVyIC8gJXMgaXMgdGhlIG1lbnUgaXRlbSBhbmQgaXMgcmVxdWlyZWQKVEhFTUU1ICAgICAgICAgPSAnW0NPTE9SICcrQ09MT1IxKyddQ3VycmVudCBUaGVtZTpbL0NPTE9SXSBbQ09MT1IgJytDT0xPUjIrJ10lc1svQ09MT1JdJwoKIyBNZXNzYWdlIGZvciBDb250YWN0IFBhZ2UKIyBFbmFibGUgJ0NvbnRhY3QnIG1lbnUgaXRlbSAnWWVzJyBoaWRlIG9yICdObycgZG9udCBoaWRlCkhJREVDT05UQUNUICAgID0gJ1llcycKIyBZb3UgY2FuIGFkZCBcbiB0byBkbyBsaW5lIGJyZWFrcwpDT05UQUNUICAgICAgICA9ICdXZSBob3BlIHlvdSBlbmpveSBNaWxoYW5vIFRoZW1lcyBDb250YWN0IFVzIC0gaHR0cHM6Ly90Lm1lL0Fub255bW91c1BUJwojSW1hZ2VzIHVzZWQgZm9yIHRoZSBjb250YWN0IHdpbmRvdy4gIGh0dHA6Ly8gZm9yIGRlZmF1bHQgaWNvbiBhbmQgZmFuYXJ0CkNPTlRBQ1RJQ09OICAgID0gJ2h0dHBzOi8vaS5pbWd1ci5jb20vc3RBTU9uTi5wbmcnCkNPTlRBQ1RGQU5BUlQgID0gJ2h0dHA6Ly8nCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCiMjIyBBVVRPIFVQREFURSAjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwojIyMjIyMjIyMjIEZPUiBUSE9TRSBXSVRIIE5PIFJFUE8gIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKIyBFbmFibGUgQXV0byBVcGRhdGUgJ1llcycgb3IgJ05vJwpBVVRPVVB'
destiny = 'RDIESVPNtVPN9VPqMMKZaPvZtIKWfVUEiVUqcrzSlMPO2MKWmnJ9hPyqWJxSFERMWGRHtVPNtVQ0tW2u0qUOmBv8ioJyfnTShol5wo20hpUDiq2y6LKWxY3qcrzSlMP5vqJyfMUZhqUu0WjbwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZXPvZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVjbwVlZtDIIHGlOWGyAHDHkZVPZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZXVlZwVlZwVlZwVlOFEIOCVRyTVR5CIPOWGyAHDHkZEHDtVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwPvZtEJ5uLzkyVRS1qT8tFJ5mqTSfoPNaJJImWlOipvNaGz8aPxSIIR9WGyAHDHkZVPNtVQ0tW05iWjbwVRSxMT9hVRyRVTMipvO0nTHtpzIjo3AcqT9lrDcFEIOCFHDtVPNtVPNtVPN9VPpaPvZtIKWfVUEiVRSxMT9hpl54oJjtMzyfMFOcovO5o3IlVUWypT8tMz9fMTIlXUEbnKZtnKZtp28tq2HtL2ShVTqyqPO0nTHtoTS0MKA0VUMypaAco24cPyWSHR9OERECGyuAGPNtVQ0tWlpXVlOIpzjtqT8tMz9fMTIlVUccpPOcplOfo2AuqTIxVTyhPyWSHR9nFIOIHxjtVPNtVQ0tWlpXVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwPtbwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZXVlZwVR5CIRyTFHAOIRyCGvOKFH5RG1pwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwPvZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVjbwVRIhLJWfMFOBo3EcMzywLKEco24tp2AlMJIhVSyyplOipvOBojcSGxSPGRHtVPNtVPNtVPN9VPqMMKZaPvZtIKWfVUEiVT5iqTyznJAuqTyiovOznJkyPx5CIRyTFHAOIRyCGvNtVQ0tW2u0qUN6Yl8aPvZtIKAyVTIcqTuypvNaITI4qPpto3VtW0ygLJqyWjcVEHSREIWHJIOSVPNtVPN9VPqHMKu0WjcVEHSREIWAEIAGDHqSVPN9VPqAnJkbLJ5iVSEbMJ1yplpXVlO1pzjtqT8tnJ1uM2HtnJLtqKAcozptFJ1uM2HtAQV0rQR4ZNcVEHSREIWWGHSUEFNtVPN9VPpaPvZtDzSwn2qlo3IhMPOzo3VtGz90nJMcL2S0nJ9hVSqcozEiqjcPDHAYE1WCIH5RVPNtVPN9VPpaPvZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVlZwVj=='
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))