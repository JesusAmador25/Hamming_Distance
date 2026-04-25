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

---

## Functions 

**... coming soon ...** 

---

## Team

<table align="center" width= 100% >
  <tr>
    <td align="center">
      <a href="https://github.com/JesusAmador25">
        <img src="https://github.com/JesusAmador25.png?size=200" width="120" alt=" Jesus Amador " />
        <br />
        <sub><b>@JesusAmador25</b></sub>
      </a>
      <br />
      <sub>Jesus Amador</sub>
    </td>
    <td align="center">
      <a href="https://github.com/robertoeduardohernandezbenitez-ux">
        <img src="https://github.com/robertoeduardohernandezbenitez-ux.png?size=200" width="120" alt=" Roberto Hernandez " />
        <br />
        <sub><b>@robertoeduardohernandezbenitez-ux</b></sub>
      </a>
      <br />
      <sub> Roberto Hernández </sub>
    </td>
    <td align="center">
      <a href="https://github.com/Belinda-Hernandez-Santamaria">
        <img src="https://github.com/Belinda-Hernandez-Santamaria.png?size=200" width="120" alt=" Belinda Hernandez "/>
        <br />
        <sub><b>@Belinda-Hernandez-Santamaria</b></sub>
      </a>
      <br />
      <sub> Belinda Hernández </sub>
    </td>
        <td align="center">
      <a href="https://github.com/Sqrt-sarai666">
        <img src="https://github.com/Sqrt-sarai666.png?size=200" width="120" alt=" Sarai Ramos "/>
        <br />
        <sub><b>@Sqrt-sarai666</b></sub>
      </a>
      <br />
      <sub> Sarai Ramos </sub>
    </td>
  </tr>
</table>

