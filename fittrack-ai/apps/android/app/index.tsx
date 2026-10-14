import React, { useEffect, useState, useRef } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  ScrollView,
  StyleSheet,
  ActivityIndicator,
  Alert,
  Share,
  AppState,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { StatusBar } from "expo-status-bar";
import * as Crypto from "expo-crypto";
import { router, useLocalSearchParams } from "expo-router";
import { api, restore, setSession, owner, ApiError } from "../src/api";
import { queue, sync, draftCount, clearOwnDrafts } from "../src/drafts";
type Food = {
  id: string;
  name: string;
  brand: string;
  calories: number | null;
  protein: number | null;
  carbs: number | null;
  fat: number | null;
  source: string;
  source_url: string;
  verification: string;
  license: string;
};
type Entry = {
  id: string;
  grams: number;
  food_id: string;
  eaten_at: string;
  version: number;
  meal_type: string;
  snapshot: { food: Food; nutrition: Record<string, number | null> };
};
type Diary = {
  items: Entry[];
  summary: Record<
    string,
    { total: number | null; knownSubtotal: number; complete: boolean }
  >;
};
const show = (v: number | null | undefined) =>
  v == null ? "Unknown" : Number(v).toFixed(1);
function today() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
export default function Home() {
  const [goal,setGoal]=useState<number|null>(null);
  const [displayName,setDisplayName]=useState("");
  const params=useLocalSearchParams<{foodQuery?:string}>();
  const actionLock=useRef(false);
  const [editing,setEditing]=useState<Entry|null>(null);
  const [editGrams,setEditGrams]=useState("");
  const [ready, setReady] = useState(false),
    [signed, setSigned] = useState(false),
    [register, setRegister] = useState(false),
    [email, setEmail] = useState(""),
    [password, setPassword] = useState(""),
    [name, setName] = useState("");
  const [tab, setTab] = useState("Today"),
    [query, setQuery] = useState(""),
    [foods, setFoods] = useState<Food[]>([]),
    [selected, setSelected] = useState<Food | null>(null),
    [grams, setGrams] = useState("100"),
    [mealType, setMealType] = useState("breakfast"),
    [date, setDate] = useState(today()),
    [diary, setDiary] = useState<Diary | null>(null),
    [pending, setPending] = useState(0),
    [busy, setBusy] = useState(false),
    [message, setMessage] = useState(""),
    [searched, setSearched] = useState(false);
  async function load() {
    setDiary(
      await api<Diary>(
        `/api/v1/meals/daily?date=${date}&zone=${encodeURIComponent(Intl.DateTimeFormat().resolvedOptions().timeZone)}`,
      ),
    );
    setPending(await draftCount());
  }
  async function action(fn: () => Promise<void>) {
    if (actionLock.current) return;
    actionLock.current=true;
    setBusy(true);
    setMessage("");
    try {
      await fn();
    } catch (e) {
      setMessage(e instanceof Error ? e.message : "Something went wrong");
      if (!owner()) {
        setSigned(false);
        setDiary(null);
        setSelected(null);
      }
    } finally {
      actionLock.current=false;
      setBusy(false);
    }
  }
  useEffect(() => {
    restore()
      .then((s) => setSigned(!!s))
      .catch(() => setMessage("Could not read secure session"))
      .finally(() => setReady(true));
  }, []);
  useEffect(() => {
    if (!signed) return;
    let alive = true;
    void Promise.all([api<{display_name:string}>('/api/v1/users/me'),api<{calories:number|null}>('/api/v1/nutrition/goals')]).then(([profile,goals])=>{if(alive){setDisplayName(profile.display_name);setGoal(goals.calories);}}).catch(e=>{if(alive)setMessage(e.message);});
    api<Diary>(
      `/api/v1/meals/daily?date=${date}&zone=${encodeURIComponent(Intl.DateTimeFormat().resolvedOptions().timeZone)}`,
    )
      .then((data) => {
        if (alive) setDiary(data);
      })
      .catch((e) => {
        if (alive){setMessage(e.message);if(!owner()){setSigned(false);setDiary(null);}}
      });
    draftCount().then((n) => {
      if (alive) setPending(n);
    }).catch(e=>{if(alive)setMessage(e.message);});
    return () => {
      alive = false;
    };
  }, [signed]);
  useEffect(() => {
    const sub = AppState.addEventListener("change", (s) => {
      if (s === "active" && owner())
        void sync()
          .then(() => draftCount())
          .then(setPending)
          .catch(() => {});
    });
    return () => sub.remove();
  }, []);
  useEffect(()=>{if(params.foodQuery){setQuery(params.foodQuery);setTab('Add food');setFoods([]);setSearched(false);}},[params.foodQuery]);
  const button = (label: string, fn: () => void, secondary = false) => (
    <Pressable
      accessibilityRole="button"
      disabled={busy}
      onPress={fn}
      style={[s.button, secondary && s.secondary, busy && { opacity: 0.5 }]}
    >
      <Text style={[s.buttonText, secondary && { color: "#33553D" }]}>
        {label}
      </Text>
    </Pressable>
  );
  const input = (
    label: string,
    value: string,
    onChange: (v: string) => void,
    secret = false,
  ) => (
    <TextInput
      accessibilityLabel={label}
      placeholder={label}
      placeholderTextColor="#758D99"
      value={value}
      onChangeText={onChange}
      secureTextEntry={secret}
      autoCapitalize="none"
      style={s.input}
    />
  );
  if (!ready)
    return (
      <SafeAreaView style={s.safe}>
        <ActivityIndicator color="#245C40" />
      </SafeAreaView>
    );
  return (
    <SafeAreaView style={s.safe}>
      <StatusBar style="dark" />
      <ScrollView
        contentContainerStyle={s.page}
        keyboardShouldPersistTaps="handled"
      >
        <View style={s.top}>
          <Text style={s.logo}>
            FitTrack
          </Text>
          <Text style={s.label}>DAILY NUTRITION</Text>
        </View>
        {!signed ? (
          <>
            <Text style={s.heading}>Good food.{"\n"}A little clarity.</Text>
            <Text style={s.muted}>
              A simple journal for your meals, portions and everyday progress.
            </Text>
            <View style={s.card}>
              <Text style={s.title}>
                {register ? "Create your account" : "Welcome back"}
              </Text>
              {register && input("Your name", name, setName)}
              {input("Email address", email, setEmail)}
              {input(
                "Password (12–64 characters)",
                password,
                setPassword,
                true,
              )}
              {button(
                register ? "Create account" : "Sign in",
                () =>
                  void action(async () => {
                    const session = await api<any>(
                      register ? "/api/v1/auth/register" : "/api/v1/auth/login",
                      "POST",
                      { email, password, displayName: name },
                    );
                    await setSession(session);
                    setPassword("");
                    setSigned(true);
                  }),
              )}
              {button(
                register
                  ? "Already registered? Sign in"
                  : "New here? Create account",
                () => setRegister(!register),
                true,
              )}
            </View>
          </>
        ) : (
          <>
            <View style={s.tabs}>
              {["Today", "Add food", "Privacy"].map((t) => (
                <Pressable
                  accessibilityRole="tab"
                  accessibilityState={{ selected: tab === t }}
                  key={t}
                  onPress={() => setTab(t)}
                  style={[s.tab, tab === t && s.active]}
                >
                  <Text
                    style={{
                      color: tab === t ? "#FFFFFF" : "#738072",
                      fontWeight: "700",
                    }}
                  >
                    {t}
                  </Text>
                </Pressable>
              ))}
            </View>
            {tab === "Today" && (
              <>
                <Text style={s.heading}>Today, on{"\n"}your plate.</Text>
                {input("Diary date YYYY-MM-DD", date, setDate)}
                <Text style={s.muted}>{displayName?`Hello, ${displayName}. `:''}{diary?`${diary.items.length} confirmed food entries.`:'Your journal is loading.'}</Text>
                <View style={s.card}>
                  <Text style={s.label}>TODAY'S ENERGY</Text>
                  <Text style={s.big}>
                    {show(diary?.summary.calories?.total)}{" "}
                    <Text style={s.unit}>kcal</Text>
                  </Text>
                  <Text style={s.muted}>{goal==null?'Set a personal target in Goals.':`Your target: ${Number(goal).toFixed(0)} kcal`}</Text>
                  {goal!=null&&goal>0&&diary?.summary.calories?.total!=null&&<View accessibilityLabel="Daily energy progress" style={{height:8,backgroundColor:'#E6EADD',borderRadius:20,overflow:'hidden'}}><View style={{height:8,backgroundColor:'#C88655',width:`${Math.min(100,Math.max(0,100*diary.summary.calories.total/goal))}%`}}/></View>}
                  <Text style={s.muted}>From the portions you confirmed.</Text>
                  <View style={s.macros}>
                    {["protein", "carbs", "fat"].map((k) => (
                      <View key={k}>
                        <Text style={s.value}>
                          {show(diary?.summary[k]?.total)}g
                        </Text>
                        <Text style={s.muted}>{k}</Text>
                      </View>
                    ))}
                  </View>
                </View>
                <Text style={s.title}>Meals</Text>
                {diary?.items.map((m) => (
                  <View style={s.card} key={m.id}>
                    <Text style={s.label}>
                      {m.meal_type.toUpperCase()} · {m.grams}g
                    </Text>
                    <Text style={s.title}>{m.snapshot.food.name}</Text>
                    <Text style={s.muted}>
                      {show(m.snapshot.nutrition.calories)} kcal ·{" "}
                      {m.snapshot.food.source}
                    </Text>
                    {button("Edit portion",()=>{setEditing(m);setEditGrams(String(m.grams));},true)}
                    {button(
                      "Delete entry",
                      () =>
                        Alert.alert(
                          "Delete this meal?",
                          "This removes the server entry.",
                          [
                            { text: "Cancel", style: "cancel" },
                            {
                              text: "Delete",
                              style: "destructive",
                              onPress: () =>
                                void action(async () => {
                                  await api("/api/v1/meals/" + m.id, "DELETE");
                                  await load();
                                }),
                            },
                          ],
                        ),
                      true,
                    )}
                  </View>
                ))}
                {diary?.items.length === 0 && (
                  <Text style={s.muted}>
                    No meals yet. Add your first food from the catalog.
                  </Text>
                )}
                {editing&&<View style={s.card}><Text style={s.title}>Edit {editing.snapshot.food.name}</Text><TextInput accessibilityLabel="Updated serving grams" keyboardType="decimal-pad" value={editGrams} onChangeText={setEditGrams} style={s.input}/>{button('Save meal changes',()=>void action(async()=>{const value=Number(editGrams);if(!Number.isFinite(value)||value<0.1||value>5000)throw new Error('Enter 0.1–5000 grams');await api('/api/v1/meals/'+editing.id,'PATCH',{foodId:editing.food_id,grams:value,mealType:editing.meal_type,eatenAt:editing.eaten_at,confirmed:true,version:editing.version});setEditing(null);await load();}))}{button('Cancel editing',()=>setEditing(null),true)}</View>}
                {button('Photos, drafts, goals & reports',()=>router.push('/tools'),true)}
                {button("Refresh diary", () => void action(load), true)}
                {button(
                  `Sync device drafts (${pending})`,
                  () =>
                    void action(async () => {
                      const count = await sync();
                      await load();
                      setMessage(`${count} meals synchronized; ${await draftCount()} drafts remain. Review pending drafts in Tools.`);
                    }),
                  true,
                )}
              </>
            )}
            {tab === "Add food" && (
              <>
                <Text style={s.heading}>
                  What is{"\n"}on your plate?
                </Text>
                <View style={s.notice}>
                  <Text style={s.title}>Meal photo analysis</Text>
                  <Text style={s.muted}>
                    Photo upload is available in Tools. Predictions require an approved trained model; manual logging works independently.
                  </Text>
                </View>
                {button("Take or choose a meal photo",()=>router.push("/tools"),true)}
                {input("Search a food or ingredient", query, setQuery)}
                {button(
                  "Search catalog",
                  () =>
                    void action(async () => {
                      const data = await api<{ items: Food[] }>(
                        `/api/v1/food/search?q=${encodeURIComponent(query)}&size=30`,
                      );
                      setFoods(data.items);
                      setSearched(true);
                    }),
                )}
                {searched && foods.length === 0 && (
                  <Text style={s.muted}>
                    No matching records. Try another spelling or import more
                    source data.
                  </Text>
                )}
                {foods.map((f) => (
                  <Pressable
                    accessibilityRole="button"
                    key={f.id}
                    onPress={() => {
                      setSelected(f);
                      setGrams("100");
                    }}
                    style={[
                      s.card,
                      selected?.id === f.id && { borderColor: "#245C40" },
                    ]}
                  >
                    <Text style={s.title}>{f.name}</Text>
                    <Text style={s.muted}>
                      {show(f.calories)} kcal / 100g · {f.source}
                    </Text>
                  </Pressable>
                ))}
                {selected && (
                  <View style={s.card}>
                    <Text style={s.title}>Review your portion</Text>
                    <Text style={s.muted}>{selected.name}</Text>
                    <TextInput
                      accessibilityLabel="Serving grams"
                      keyboardType="decimal-pad"
                      value={grams}
                      onChangeText={setGrams}
                      style={s.input}
                    />
                    <Text style={s.muted}>
                      Enter grams measured by you. Prepared dish values vary
                      with ingredients.
                    </Text>
                    <View style={s.tabs}>
                      {["breakfast", "lunch", "dinner", "snack"].map((t) => (
                        <Pressable key={t} onPress={() => setMealType(t)}>
                          <Text
                            style={{
                              color: mealType === t ? "#245C40" : "#778474",
                              paddingVertical: 16,
                            }}
                          >
                            {t}
                          </Text>
                        </Pressable>
                      ))}
                    </View>
                    <Text style={s.value}>
                      {show(
                        selected.calories == null
                          ? null
                          : (selected.calories * Number(grams)) / 100,
                      )}{" "}
                      kcal
                    </Text>
                    <Text style={s.muted}>
                      {selected.source} · {selected.license} ·{" "}
                      {selected.verification}
                    </Text>
                    <Text selectable style={s.muted}>
                      {selected.source_url}
                    </Text>
                    {button(
                      "Confirm portion & save",
                      () =>
                        void action(async () => {
                          const g = Number(grams);
                          if (!Number.isFinite(g) || g < 0.1 || g > 5000)
                            throw new Error("Enter 0.1–5000 grams");
                          await queue({
                            foodId: selected.id,
                            grams: g,
                            mealType,
                            eatenAt: new Date().toISOString(),
                            idempotencyKey: Crypto.randomUUID(),
                            confirmed: true,
                          });
                          setSelected(null);
                          setPending(await draftCount());
                          try {
                            await sync();
                            await load();
                            setMessage((await draftCount())>0?"A draft is still waiting to sync. Review it in Tools.":"Meal saved to your diary.");
                            setTab("Today");
                          } catch (e) {
                            setMessage(
                              "Saved as a device draft. Sync again when connected. " +
                                (e instanceof Error ? e.message : ""),
                            );
                          }
                        }),
                    )}
                  </View>
                )}
              </>
            )}
            {tab === "Privacy" && (
              <>
                <Text style={s.heading}>Your food.{"\n"}Your data.</Text>
                <View style={s.card}>
                  <Text style={s.title}>You stay in control</Text>
                  <Text style={s.muted}>
                    Photos upload only when you tap Analyze and are processed without persistent storage. Device drafts are
                    scoped to your account and kept until synchronized. Drafts
                    use local SQLite without additional database encryption.
                    Tokens use secure device storage.
                  </Text>
                  {button(
                    "Export my server data",
                    () =>
                      void action(async () => {
                        const data = await api("/api/v1/users/me/export");
                        await Share.share({
                          message: JSON.stringify(data, null, 2),
                        });
                      }),
                    true,
                  )}
                  {button(
                    "Sign out",
                    () =>
                      void action(async () => {
                        let notice='Signed out.';
                        try {await api("/api/v1/auth/logout", "POST");} catch(e){if(!(e instanceof ApiError&&e.retryable))throw e;notice='Signed out on this device. Server sessions could not be revoked while offline.';}
                        await setSession(null);setMessage(notice);
                        setSigned(false);
                        setDiary(null);
                        setSelected(null);
                      }),
                    true,
                  )}
                  {button(
                    "Delete my account",
                    () =>
                      Alert.alert(
                        "Permanently delete account?",
                        "Meals, sessions and account data will be deleted from the live database. Operator backups may follow a separate retention period.",
                        [
                          { text: "Cancel", style: "cancel" },
                          {
                            text: "Delete account",
                            style: "destructive",
                            onPress: () =>
                              void action(async () => {
                                const id = owner()!;
                                await api("/api/v1/users/me", "DELETE");
                                try {await clearOwnDrafts(id);} finally {await setSession(null);setSigned(false);setDiary(null);setSelected(null);}
                                setSigned(false);
                                setDiary(null);
                                setSelected(null);
                              }),
                          },
                        ],
                      ),
                    true,
                  )}
                </View>
              </>
            )}
          </>
        )}
        {busy && <ActivityIndicator color="#245C40" style={{ margin: 20 }} />}
        {!!message && (
          <Text accessibilityRole="alert" style={s.message}>
            {message}
          </Text>
        )}
        <Text style={s.footer}>A LITTLE MORE AWARE, EVERY DAY</Text>
      </ScrollView>
    </SafeAreaView>
  );
}
const s = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#F7F5EE" },
  page: { padding: 24, paddingBottom: 48, gap: 16 },
  top: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 16,
  },
  logo: { fontWeight: "700", fontSize: 20, color: "#20382B", letterSpacing: -0.5 },
  label: {
    color: "#788575",
    fontSize: 10,
    letterSpacing: 1.6,
    fontWeight: "700",
  },
  heading: {
    fontSize: 36,
    lineHeight: 43,
    fontWeight: "700",
    color: "#20382B",
    letterSpacing: -1.4,
    marginVertical: 12,
  },
  muted: { color: "#738072", fontSize: 13, lineHeight: 21 },
  card: {
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#E2E5DB",
    borderRadius: 24,
    padding: 22,
    gap: 12,
  },
  title: { fontSize: 18, color: "#20382B", fontWeight: "600" },
  input: {
    backgroundColor: "#F1F3EA",
    borderWidth: 1,
    borderColor: "#DDE3D7",
    color: "#20382B",
    padding: 16,
    borderRadius: 14,
    fontSize: 16,
    minHeight: 52,
  },
  button: {
    backgroundColor: "#245C40",
    padding: 17,
    borderRadius: 14,
    alignItems: "center",
    minHeight: 52,
  },
  buttonText: { color: "#FFFFFF", fontWeight: "800", fontSize: 14 },
  secondary: { backgroundColor: "#E8EEE2" },
  tabs: { flexDirection: "row", justifyContent: "space-between", gap: 8 },
  tab: { paddingVertical: 14, paddingHorizontal: 18, borderRadius: 30 },
  active: { backgroundColor: "#245C40" },
  big: { fontSize: 48, color: "#245C40", fontWeight: "700" },
  unit: { fontSize: 18, color: "#738072" },
  macros: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingTop: 18,
    borderTopWidth: 1,
    borderTopColor: "#E8EBE1",
  },
  value: { fontSize: 23, fontWeight: "600", color: "#20382B" },
  notice: {
    padding: 20,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "#DDE3D7",
    backgroundColor: "#EEF2E7",
    gap: 8,
  },
  message: {
    color: "#8A562D",
    backgroundColor: "#F8EEE0",
    padding: 16,
    borderRadius: 12,
    lineHeight: 21,
  },
  footer: {
    fontSize: 10,
    letterSpacing: 2,
    textAlign: "center",
    color: "#8A9586",
    marginTop: 24,
  },
});
