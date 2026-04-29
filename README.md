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
## Updated Table of Bounds for Binary Codes of Length Less than 25, with Extension for $d > 10$

| n  | d=4           | d=6          | d=8         | d=10      | d=12    | d=14 | d=16 |
|----|---------------|--------------|-------------|-----------|---------|------|------|
| 6  | 4             | 2            | 1           | 1         | 1       | 1    | 1    |
| 7  | 8             | 2            | 1           | 1         | 1       | 1    | 1    |
| 8  | 16            | 2            | 2           | 1         | 1       | 1    | 1    |
| 9  | 20            | 4            | 2           | 1         | 1       | 1    | 1    |
| 10 | 40            | 6            | 2           | 2         | 1       | 1    | 1    |
| 11 | 72            | 12           | 2           | 2         | 1       | 1    | 1    |
| 12 | 144           | 24           | 4           | 2         | 2       | 1    | 1    |
| 13 | 256           | 32           | 4           | 2         | 2       | 1    | 1    |
| 14 | 512           | 64           | 8           | 2         | 2       | 2    | 1    |
| 15 | 1024          | 128          | 16          | 4         | 2       | 2    | 1    |
| 16 | 2048          | 256          | 32          | 4         | 2       | 2    | 2    |
| 17 | 2816-3276     | 258-340      | 36          | 6         | 2       | 2    | 2    |
| 18 | 5632-6552     | 512-673      | 64          | 10        | 4       | 2    | 2    |
| 19 | 10496-13104   | 1024-1237    | 128         | 20        | 4       | 2    | 2    |
| 20 | 20480-26168   | 2048-2279    | 256         | 40        | 6       | 2    | 2    |
| 21 | 40960-43688   | 2560-4096    | 512         | 42-47     | 8       | 4    | 2    |
| 22 | 81920-87333   | 4096-6941    | 1024        | 64-84     | 12      | 4    | 2    |
| 23 | 163840-172361 | 8192-13674   | 2048        | 80-150    | 24      | 4    | 2    |
| 24 | 327680-344308 | 16384-24106  | 4096        | 136-268   | 48      | 6    | 4    |
| 25 | 2^19-599184   | 17920-47538  | 4096-5421   | 192-466   | 52-55   | 8    | 4    |
| 26 | 2^20-1198368  | 32768-84260  | 4104-9275   | 384-836   | 64-96   | 14   | 4    |
| 27 | 2^21-2396736  | 65536-157285 | 8192-17099  | 512-1585  | 128-169 | 28   | 6    |
| 28 | 2^22-4792950  | 131072-291269| 16384-32151 | 1024-2817 | 178-288 | 56   | 8    |

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

