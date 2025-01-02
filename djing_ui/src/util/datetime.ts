import { DateTime } from 'luxon';

export const formatToUTCDateTime = (dateStr: string): string => {
  const dt = DateTime.fromISO(dateStr, { zone: 'utc' });
  return dt.toFormat("MM/dd/yyyy, hh:mm a 'UTC'");
}