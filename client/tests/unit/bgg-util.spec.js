import {expect, test} from 'vitest'
import $ from "jquery";
import {bggId, createItemWithPrimaryName, displayName, primaryName, searchBgg, yearPublished} from '@/util/bgg-util'

test('bggId', () => {
  test('returns the id attribute of a bgg entry it is passed', () => {
    const item = $.parseXML('<items><item type="boardgame" id="2129"><name type="primary" value="Crossbows and Catapults"/><yearpublished value="1983"/></item></items>').documentElement.getElementsByTagName("item")[0]
    expect(bggId(item)).toMatch('2129')
  })

  test('returns null when passed a non bgg entry', () => {
    const item = $.parseXML('<items><item type="boardgame"><name value="Some Obscure Game"/></item></items>').documentElement.getElementsByTagName("item")[0]
    expect(bggId(item)).toBeNull()
  })
})


test('primaryName', () => {
  test('returns the first name value of an entry it is passed without a primary name', () => {
    const item = $.parseXML('<items><item type="boardgame"><name value="First"/><name value="Second"/></item></items>').documentElement.getElementsByTagName("item")[0]
    expect(primaryName(item)).toMatch('First')
  })

  test('returns the primary name value of an entry it is passed event if that name element is not first', () => {
    const item = $.parseXML('<items><item type="boardgame"><name value="First"/><name type="primary" value="Primary"/></item></items>').documentElement.getElementsByTagName("item")[0]
    expect(primaryName(item)).toMatch('Primary')
  })
})


test('yearPublished', () => {
  test('returns the yearpublished value of an entry it is passed', () => {
    const item = $.parseXML('<items><item type="boardgame" id="2129"><name type="primary" value="Crossbows and Catapults"/><yearpublished value="1983"/></item></items>').documentElement.getElementsByTagName("item")[0]
    expect(yearPublished(item)).toMatch('1983')
  })

  test('returns null when passed an entry without a yearpublished element', () => {
    const item = $.parseXML('<items><item type="boardgame"><name value="Some Obscure Game"/></item></items>').documentElement.getElementsByTagName("item")[0]
    expect(yearPublished(item)).toBeNull()
  })
})


test('displayName', () => {
  test('returns the primaryName (yearPublished) of an entry it is passed', () => {
    const item = $.parseXML('<items><item type="boardgame"><name value="Some Obscure Recent Game"/><yearpublished value="2023"/></item></items>').documentElement.getElementsByTagName("item")[0]
    expect(displayName(item)).toBe('Some Obscure Recent Game (2023)')
  })

  test('returns just the primaryName of an entry it is passed with no yearPublished', () => {
    const item = $.parseXML('<items><item type="boardgame"><name value="Some Obscure Game"/></item></items>').documentElement.getElementsByTagName("item")[0]
    expect(displayName(item)).toBe('Some Obscure Game')
  })
})


test('createItemWithPrimaryName', () => {
  test('returns an item with a bggId of "none"', () => {
    expect(bggId(createItemWithPrimaryName('There is no game with this title'))).toBe("none")
  })

  test('returns an item whose primaryName is the value of the parameter it is passed', () => {
    expect(primaryName(createItemWithPrimaryName('There is no game with this title'))).toBe('There is no game with this title')
  })

  test('returns an item with null yearPublished', () => {
    expect(yearPublished(createItemWithPrimaryName('There is no game with this title'))).toBeNull()
  })

  test('returns an item whose displayName is the value of the parameter it is passed', () => {
    expect(displayName(createItemWithPrimaryName('There is no game with this title'))).toBe('There is no game with this title')
  })
})


test('searchBgg', () => {
  process.env.BGG_BASE_URL = 'https://boardgamegeek.com'
  test('queries BoardGameGeek', async () => {
    const items = await searchBgg('Senet e Tablan')
    expect(items.length).toBe(1)
    const item = items[0]
    expect(bggId(item)).toBe('328628')
    expect(primaryName(item)).toBe('Senet e Tablan')
    expect(yearPublished(item)).toBeNull()
    expect(displayName(item)).toBe('Senet e Tablan')
  })

  test('combines with createItemWithPrimaryName', async () => {
    const promise = searchBgg('Senet e Tablan').then(items => items.concat([createItemWithPrimaryName('Senet e Tablan')]))
    const items = await promise
    expect(items.length).toBe(2)
    const item = items[1]
    expect(primaryName(item)).toBe('Senet e Tablan')
    expect(yearPublished(item)).toBeNull()
    expect(displayName(item)).toBe('Senet e Tablan')
  })

  test('combines with createItemWithPrimaryName even when no BoardGameGeek item exists', async () => {
    const promise = searchBgg('There is no game with this title').then(items => items.concat([createItemWithPrimaryName('There is no game with this title')]))
    const items = await promise
    expect(items.length).toBe(1)
    const item = items[0]
    expect(primaryName(item)).toBe('There is no game with this title')
    expect(yearPublished(item)).toBeNull()
    expect(displayName(item)).toBe('There is no game with this title')
  })
})
