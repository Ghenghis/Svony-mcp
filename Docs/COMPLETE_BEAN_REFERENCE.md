# 📦 COMPLETE BEAN FIELD REFERENCE
## Extracted via RAG - Phase 2 Complete

---

## PlayerInfoBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| userId | int | Player ID |
| userName | String | Player name |
| alliance | String | Alliance name |
| prestige | int | Prestige points |
| honor | int | Honor points |
| lastLoginTime | Number | Last login timestamp |
| bdenyotherplayer | int | Deny other players flag |
| date | String | Registration date |
| starlv | int | Star level |
| effortPoint | int | Effort points |
| rank | int | Player rank |

---

## CastleBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| castleId | int | Castle ID |
| name | String | Castle name |
| status | int | Castle status |
| level | int | Town Hall level |
| positionId | int | Map position |
| strTroop | TroopStrBean | Troop strength |
| buildings | Array | Building list |
| buffs | Array[BuffBean] | Active buffs |
| resource | CastleResourceBean | Resources |

---

## CastleResourceBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| food | ResourceInfoBean | Food resource |
| wood | ResourceInfoBean | Wood resource |
| stone | ResourceInfoBean | Stone resource |
| iron | ResourceInfoBean | Iron resource |
| gold | Number | Gold amount |
| support | int | Population support |
| workPeople | int | Working population |

---

## HeroBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| heroId | int | Hero ID |
| name | String | Hero name |
| level | int | Hero level |
| experience | int | Experience points |
| stratagem | int | Politics attribute |
| attack | Number | Attack attribute |
| defence | int | Defense attribute |
| intelligence | int | Intelligence |
| managementAdded | int | Management bonus |
| upgradeExp | int | Upgrade experience |
| powerAdded | int | Power bonus |
| status | int | Hero status (0-7) |
| buffsArray | ArrayCollection | Hero buffs |
| equipmentbean | Array | Equipment |

---

## ArmyBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| armyId | int | Army ID |
| heroId | int | Leading hero |
| castleId | int | Origin castle |
| targetX | int | Target X coord |
| targetY | int | Target Y coord |
| missionType | int | Mission type |
| troops | Array | Troop composition |
| startTime | Number | March start |
| endTime | Number | Arrival time |
| direction | int | Return/outbound |

---

## BuffBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| buffId | int | Buff ID |
| typeId | int | Buff type |
| value | Number | Buff value |
| endTime | Number | Expiration time |
| description | String | Buff description |

---

## BuildingBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| positionId | int | Building position |
| typeId | int | Building type |
| level | int | Building level |
| status | int | Build status |
| startTime | Number | Construction start |
| endTime | Number | Construction end |
| help | int | Help requests |
| appearance | int | Visual appearance |
| name | String | Building name |

---

## MapCastleBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| castleId | int | Castle ID |
| id | int | Map ID |
| name | String | Castle name |
| userName | String | Owner name |
| allianceName | String | Alliance |
| x | int | X coordinate |
| y | int | Y coordinate |
| level | int | Castle level |
| state | int | State/region |
| colonialRelation | int | Colonial relation |
| colonialStatus | int | Colonial status |
| declaredWarStartTime | Number | War declaration time |
| flag | int | Flag type |
| honor | int | Honor points |
| prestige | int | Prestige points |

---

## EquipmentBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| equipmentId | int | Equipment ID |
| typeId | int | Equipment type |
| name | String | Item name |
| level | int | Enhancement level |
| star | int | Star rating |
| gems | Array | Gem slots |
| addAttribute | int | Bonus attribute |
| addAttributeType | int | Attribute type |
| attack | Number | Attack bonus |
| defence | Number | Defense bonus |

---

## ItemBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| itemId | int | Item ID |
| typeId | int | Item type |
| name | String | Item name |
| count | int | Quantity |
| description | String | Description |
| usable | Boolean | Can be used |
| tradeable | Boolean | Can be traded |

---

## TroopBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| typeId | int | Troop type |
| count | int | Troop count |
| injured | int | Injured count |

---

## AllianceInfoResponse

**Package:** `com.evony.common.module.alliance`

| Field | Type | Description |
|-------|------|-------------|
| packageId | Number | Package ID |
| msg | String | Message |
| allinaceInfo | String | Alliance info |
| creator | String | Creator name |
| leader | String | Leader name |
| prestigeCount | int | Total prestige |
| memberCount | int | Member count |
| errorMsg | String | Error message |

---

## AllianceAddPlayerInfoBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| prestige | int | Player prestige |
| userName | String | Player name |
| invitePerson | String | Inviter name |
| rank | int | Player rank |
| castleCount | int | Castle count |
| inviteTime | Number | Invite timestamp |

---

## QuestBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| questId | int | Quest ID |
| typeId | int | Quest type |
| name | String | Quest name |
| description | String | Description |
| status | int | Quest status |
| progress | int | Current progress |
| target | int | Target amount |
| reward | Object | Reward data |

---

## ReportBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| reportId | int | Report ID |
| typeId | int | Report type |
| title | String | Report title |
| time | Number | Report time |
| isRead | Boolean | Read status |
| startPos | String | Start position |
| endPos | String | End position |

---

## MailBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| mailId | int | Mail ID |
| typeId | int | Mail type |
| title | String | Mail title |
| content | String | Mail content |
| sender | String | Sender name |
| time | Number | Send time |
| isRead | Boolean | Read status |
| hasAttachment | Boolean | Has attachment |

---

## TradeBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| tradeId | int | Trade ID |
| resourceType | int | Resource type |
| amount | int | Resource amount |
| price | Number | Price per unit |
| totalPrice | Number | Total price |
| status | int | Trade status |
| sellerName | String | Seller name |

---

## TechBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| techId | int | Technology ID |
| typeId | int | Tech type |
| level | int | Current level |
| status | int | Research status |
| startTime | Number | Start time |
| endTime | Number | End time |

---

## FortificationsBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| trap | int | Trap count |
| abatis | int | Abatis count |
| archerTower | int | Archer tower count |
| rollingLogs | int | Rolling logs |
| rockfall | int | Rockfall count |
| trebuche | int | Trebuchet count |

---

## NpcBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| id | int | NPC ID |
| level | int | NPC level |
| x | int | X coordinate |
| y | int | Y coordinate |
| troops | Object | Troop composition |

---

## ColonyBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| colonyId | int | Colony ID |
| castleId | int | Parent castle |
| x | int | X coordinate |
| y | int | Y coordinate |
| level | int | Colony level |
| status | int | Colony status |

---

## TroopStrBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| worker | int | Workers |
| warrior | int | Warriors |
| scout | int | Scouts |
| pikeman | int | Pikemen |
| swordsman | int | Swordsmen |
| archer | int | Archers |
| cavalry | int | Cavalry |
| cataphract | int | Cataphracts |
| transporter | int | Transporters |
| ballista | int | Ballistas |
| ram | int | Battering rams |
| catapult | int | Catapults |

---

## ResourceInfoBean

**Package:** `com.evony.common.beans`

| Field | Type | Description |
|-------|------|-------------|
| amount | Number | Current amount |
| maxStore | Number | Max storage |
| produceRate | Number | Production rate |
| workPeople | int | Workers |

---

*Phase 2 Complete - 25+ Bean Classes Documented*
*Generated via RAG Full Access Mode*
