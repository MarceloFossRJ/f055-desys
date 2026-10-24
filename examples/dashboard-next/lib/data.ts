import type { Point } from '@/components/chart';

export const streams: Point[] = [
  { label: 'May', current: 412_000, previous: 388_000 },
  { label: 'Jun', current: 468_000, previous: 401_000 },
  { label: 'Jul', current: 445_000, previous: 437_000 },
  { label: 'Aug', current: 521_000, previous: 452_000 },
  { label: 'Sep', current: 604_000, previous: 478_000 },
  { label: 'Oct', current: 662_000, previous: 509_000 },
];

export type Status = 'Live' | 'In review' | 'Scheduled' | 'Takedown';

export type Release = {
  id: string;
  title: string;
  artist: string;
  type: 'Single' | 'EP' | 'Album';
  status: Status;
  streams: number;
  royalties: number;
  reviewer: string | null;
};

export const releases: Release[] = [
  { id: 'F055-0142', title: 'Night Signals',      artist: 'F055',          type: 'Single', status: 'Live',      streams: 184_320, royalties: 1_412.88, reviewer: 'Eddie Lake' },
  { id: 'F055-0141', title: 'Kreuzberg Tapes',    artist: 'Lúcia Andrade', type: 'EP',     status: 'Live',      streams: 96_204,  royalties: 742.19,   reviewer: 'Eddie Lake' },
  { id: 'F055-0140', title: 'Static Garden',      artist: 'Mø Verde',      type: 'Album',  status: 'In review', streams: 0,       royalties: 0,        reviewer: null },
  { id: 'F055-0139', title: 'Hold / Release',     artist: 'F055',          type: 'Single', status: 'Scheduled', streams: 0,       royalties: 0,        reviewer: 'Jamik Tashpulatov' },
  { id: 'F055-0138', title: 'Copper Wires',       artist: 'Teodoro Reis',  type: 'EP',     status: 'Live',      streams: 61_877,  royalties: 488.05,   reviewer: 'Jamik Tashpulatov' },
  { id: 'F055-0137', title: 'Low Tide, Repeated', artist: 'Mø Verde',      type: 'Single', status: 'Live',      streams: 44_190,  royalties: 331.42,   reviewer: 'Eddie Lake' },
  { id: 'F055-0136', title: 'Afterimage',         artist: 'Lúcia Andrade', type: 'Album',  status: 'Takedown',  streams: 12_045,  royalties: 94.60,    reviewer: 'Jamik Tashpulatov' },
  { id: 'F055-0135', title: 'Pirate Radio Hymns', artist: 'F055',          type: 'EP',     status: 'In review', streams: 0,       royalties: 0,        reviewer: null },
];

export const stats = [
  { label: 'Monthly streams',  value: '662,041', delta: '+9.6%',  up: true,  note: 'Trending up this month',   sub: 'Six straight months of growth' },
  { label: 'Net royalties',    value: '€5,118',  delta: '+12.5%', up: true,  note: 'Above projection',          sub: 'Paid out on the 15th' },
  { label: 'Active releases',  value: '142',     delta: '+4',     up: true,  note: 'Four added this period',    sub: 'Two still in review' },
  { label: 'Skip rate',        value: '22.4%',   delta: '-2.1%',  up: false, note: 'Down 2.1% this period',     sub: 'Lower is better' },
];
