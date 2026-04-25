# Maximum Binary Code Size Calculator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Status badge](https://img.shields.io/badge/status%20-in%20progress-orange)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python library that computes **A(n, d)** — the maximum number of binary *n*‑tuples that can be placed in a code of length *n* with minimum Hamming distance *d*, this is designed to exactly compute A(9, 4) and A(10, 4), while also providing a reusable framework for other parameters.

---

## Background

Error‑correcting codes are fundamental in digital communications and data storage. The function **A(n, d)** represents the largest possible size of a binary block code of length *n* and minimum distance *d*. Determining exact values of A(n, d) is a notoriously difficult combinatorial problem; many values are still unknown for a lot  **n**.

For the parameters (9, 4) and (10, 4), the exact values are known:
- **A(9, 4) = 20**
- **A(10, 4) = 40**

This project provides a verified, self‑contained computation of these maxima using efficient search algorithms and theoretical upper bounds.

---

## Features

- **Exact computation** of A(9, 4) and A(10, 4).
- Modular Python library that can be extended to other (n, d) pairs.
- Implementation of pruning techniques to keep the search feasible.

---

## Installation

**... coming soon ...** 

## Contributors

| [Avatar](Perfil GitHub) | Nombre | Enlace |
| :---: | :--- | :--- |
| ![Avatar](URL_imagen) | ** Jesus Amador ** | [GitHub](https://github.com/JesusAmador25) |   
| ![Avatar](URL_imagen) | ** Roberto Hernandez ** | [GitHub](https://github.com/robertoeduardohernandezbenitez-ux) |
| ![Avatar](URL_imagen) | ** Belinda Hernandez ** | [GitHub](https://github.com/Belinda-Hernandez-Santamaria) |
| ![Avatar](URL_imagen) | ** Sarai Ramos ** | [GitHub](https://github.com/Sqrt-sarai666) |


