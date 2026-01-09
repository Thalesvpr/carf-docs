import { describe, expect, test } from 'bun:test'
import { CNPJ } from './cnpj'
import { ValidationError } from './cpf'

describe('CNPJ', () => {
  describe('validation', () => {
    test('should accept valid CNPJ', () => {
      expect(() => new CNPJ('11.222.333/0001-81')).not.toThrow()
      expect(() => new CNPJ('11222333000181')).not.toThrow()
    })

    test('should reject invalid CNPJ', () => {
      expect(() => new CNPJ('11.222.333/0001-82')).toThrow(ValidationError)
      expect(() => new CNPJ('11.222.333/0001-80')).toThrow(ValidationError)
    })

    test('should reject known invalid sequences', () => {
      expect(() => new CNPJ('00.000.000/0000-00')).toThrow(ValidationError)
      expect(() => new CNPJ('11.111.111/1111-11')).toThrow(ValidationError)
      expect(() => new CNPJ('22.222.222/2222-22')).toThrow(ValidationError)
    })

    test('should reject CNPJ with wrong length', () => {
      expect(() => new CNPJ('123')).toThrow(ValidationError)
      expect(() => new CNPJ('123456789012345678')).toThrow(ValidationError)
    })

    test('should reject empty CNPJ', () => {
      expect(() => new CNPJ('')).toThrow(ValidationError)
    })
  })

  describe('formatting', () => {
    test('should format CNPJ correctly', () => {
      const cnpj = new CNPJ('11222333000181')
      expect(cnpj.format()).toBe('11.222.333/0001-81')
    })

    test('should preserve formatting when already formatted', () => {
      const cnpj = new CNPJ('11.222.333/0001-81')
      expect(cnpj.format()).toBe('11.222.333/0001-81')
    })
  })

  describe('normalization', () => {
    test('should return raw digits with toString()', () => {
      const cnpj = new CNPJ('11.222.333/0001-81')
      expect(cnpj.toString()).toBe('11222333000181')
    })

    test('should normalize in JSON serialization', () => {
      const cnpj = new CNPJ('11.222.333/0001-81')
      expect(JSON.stringify({ cnpj })).toBe('{"cnpj":"11222333000181"}')
    })
  })

  describe('equality', () => {
    test('should consider equal CNPJs with same value', () => {
      const cnpj1 = new CNPJ('11.222.333/0001-81')
      const cnpj2 = new CNPJ('11222333000181')
      expect(cnpj1.equals(cnpj2)).toBe(true)
    })

    test('should consider different CNPJs not equal', () => {
      const cnpj1 = new CNPJ('11.222.333/0001-81')
      const cnpj2 = new CNPJ('11.444.777/0001-61') // Different CNPJ
      expect(cnpj1.equals(cnpj2)).toBe(false)
    })
  })
})
